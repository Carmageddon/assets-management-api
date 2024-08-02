from flask_restx import Resource, Namespace, fields
from bson.objectid import ObjectId
from .models import AssetSchema
from .. import mongo
from ..utils import validate_payload
import uuid

api = Namespace('assets', description='Assets operations')

asset_model = api.model('Asset', {
    'id': fields.String(required=True, description='The asset identifier'),
    'name': fields.String(required=True, description='The asset name'),
    'type': fields.String(required=True, description='The asset type'),
    'tags': fields.List(fields.Nested(api.model('Tag', {
        'key': fields.String(required=True, description='The tag key'),
        'value': fields.String(required=True, description='The tag value'),
    }))),
    'cloud_account': fields.Nested(api.model('CloudAccount', {
        'id': fields.String(required=True, description='The cloud account ID'),
        'name': fields.String(required=True, description='The cloud account name'),
    }), required=True),
    'owner_id': fields.String(required=True, description='The owner ID'),
    'region': fields.String(required=True, description='The asset region'),
    'group_name': fields.String(description='The group name of the asset')
})

@api.route('/')
class AssetList(Resource):
    @api.doc('list_assets')
    @api.marshal_list_with(asset_model)
    def get(self):
        assets = list(mongo.db.assets.find())
        for asset in assets:
            asset["_id"] = str(asset["_id"])
        return assets

    @api.doc('create_asset')
    @api.expect(asset_model)
    @api.response(201, 'Asset created successfully')
    @validate_payload(schema=AssetSchema)
    def post(self, payload):
        payload["_id"] = str(uuid.uuid4())
        mongo.db.assets.insert_one(payload)
        return {'message': 'Asset created successfully', 'id': payload["_id"]}, 201

@api.route('/<string:asset_id>')
@api.param('asset_id', 'The asset identifier')
class AssetResource(Resource):
    @api.doc('get_asset')
    @api.marshal_with(asset_model)
    @api.response(404, 'Asset not found')
    def get(self, asset_id):
        asset = mongo.db.assets.find_one({"_id": ObjectId(asset_id)})
        if asset:
            asset["_id"] = str(asset["_id"])
            return asset
        else:
            return {'message': 'Asset not found'}, 404

    @api.doc('update_asset')
    @api.expect(asset_model)
    @api.response(200, 'Asset updated successfully')
    @api.response(404, 'Asset not found')
    @validate_payload(schema=AssetSchema)
    def put(self, asset_id, payload):
        result = mongo.db.assets.update_one({"_id": ObjectId(asset_id)}, {"$set": payload})
        if result.matched_count == 0:
            return {'message': 'Asset not found'}, 404
        return {'message': 'Asset updated successfully'}, 200
