import uuid
from flask_restx import Namespace, Resource, fields
from flask import request
from bson.objectid import ObjectId
from .utils import clean_payload
from .. import mongo
import logging

logger = logging.getLogger(__name__)

api = Namespace('rules', description='Rules operations')

# Define a key-value model for tags
tag_model = api.model('Tag', {
    'key': fields.String(description='The key of the tag'),
    'value': fields.String(description='The value of the tag')
})

# Define condition model
condition_model = api.model('Condition', {
    'type': fields.String(description='The type of asset'),
    'tags': fields.List(fields.Nested(tag_model), description='The tags of the asset'),
    'name_contains': fields.String(description='Substring that must be present in the asset name'),
})

# Define logical model for nested conditions
logical_model = api.model('LogicalCondition', {
    'AND': fields.List(fields.Nested(api.model('SubCondition', {
        'type': fields.String(description='The type of asset'),
        'tags': fields.List(fields.Nested(tag_model), description='The tags of the asset'),
        'name_contains': fields.String(description='Substring that must be present in the asset name'),
        'AND': fields.List(fields.Nested(condition_model)),
        'OR': fields.List(fields.Nested(condition_model)),
    }))),
    'OR': fields.List(fields.Nested(api.model('SubCondition', {
        'type': fields.String(description='The type of asset'),
        'tags': fields.List(fields.Nested(tag_model), description='The tags of the asset'),
        'name_contains': fields.String(description='Substring that must be present in the asset name'),
        'AND': fields.List(fields.Nested(condition_model)),
        'OR': fields.List(fields.Nested(condition_model)),
    })))
})

# Define rule model
rule_model = api.model('Rule', {
    'owner_id': fields.String(required=True, description='The owner identifier'),
    'group_name': fields.String(required=True, description='The group name'),
    'conditions': fields.Nested(logical_model, required=True),
})

@api.route('/')
class RuleResource(Resource):
    @api.doc('list_rules')
    @api.marshal_list_with(rule_model)
    def get(self):
        """List all rules or filter by owner_id"""
        owner_id = request.args.get('owner_id')
        if owner_id:
            rules = list(mongo.db.rules.find({"owner_id": owner_id}))
        else:
            rules = list(mongo.db.rules.find())
        for rule in rules:
            rule["_id"] = str(rule["_id"])
        return rules

    @api.doc('create_rule')
    @api.expect(rule_model)
    @api.response(201, 'Rule created successfully')
    def post(self):
        """Create a new rule"""
        payload = request.json
        payload["_id"] = str(uuid.uuid4())
        cleaned_payload = clean_payload(payload)
        logger.debug(f"Payload: {payload}")
        logger.debug(f"Payload: {cleaned_payload}")

        try:
            mongo.db.rules.insert_one(payload)
            response = {'message': 'Rule created successfully', 'id': payload["_id"]}
            logger.debug(f"Response: {response}")
            return response, 201
        except Exception as e:
            logger.error(f"Error: {e}")
            response = {'message': 'Error occurred while creating the rule', 'error': str(e)}
            logger.error(f"Error Response: {response}")
            return response, 500

@api.route('/<string:rule_id>')
@api.param('rule_id', 'The rule identifier')
class RuleDetailResource(Resource):
    @api.doc('update_rule')
    @api.expect(rule_model)
    @api.response(200, 'Rule updated successfully')
    @api.response(404, 'Rule not found')
    def put(self, rule_id):
        """Update an existing rule"""
        payload = request.json
        cleaned_payload = clean_payload(payload)
        logger.debug(f"Payload: {cleaned_payload}")

        # Manual validation
        if not payload.get('owner_id') or not payload.get('group_name') or not payload.get('conditions'):
            logger.error("Validation error: Missing required fields")
            return {'message': 'Validation error: Missing required fields'}, 400

        try:
            result = mongo.db.rules.update_one({"_id": ObjectId(rule_id)}, {"$set": payload})
            if result.matched_count == 0:
                logger.error("Rule not found")
                return {'message': 'Rule not found'}, 404
            response = {'message': 'Rule updated successfully'}
            logger.debug(f"Response: {response}")
            return response, 200
        except Exception as e:
            logger.error(f"Error: {e}")
            response = {'message': 'Error occurred while updating the rule', 'error': str(e)}
            logger.error(f"Error Response: {response}")
            return response, 500

    @api.doc('get_rule')
    @api.marshal_with(rule_model)
    @api.response(404, 'Rule not found')
    def get(self, rule_id):
        """Retrieve a rule by its ID"""
        rule = mongo.db.rules.find_one({"_id": ObjectId(rule_id)})
        if rule:
            rule["_id"] = str(rule["_id"])
            return rule
        else:
            return {'message': 'Rule not found'}, 404
