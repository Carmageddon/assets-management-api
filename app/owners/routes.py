from flask_restx import Namespace, Resource
from pymongo import UpdateOne
from app import mongo
from app.owners.utils import evaluate_condition
import logging


logger = logging.getLogger(__name__)

api = Namespace('owners', description='Operations related to owners')

def matches_rule(asset, rule):
    conditions = rule.get("conditions", {})
    return evaluate_condition(asset, conditions)

@api.route('/<owner_id>/apply-rules')
class ApplyRules(Resource):
    def post(self, owner_id):
        # Fetch relevant rules for the owner
        rules = list(mongo.db.rules.find({"owner_id": owner_id}).sort("order", 1))

        # Fetch relevant assets for the owner
        assets = list(mongo.db.assets.find({"owner_id": owner_id}))

        # Apply rules to assets
        bulk_operations = []
        for asset in assets:
            group_names = []
            for rule in rules:
                if matches_rule(asset, rule):
                    group_names.append(rule["group_name"])
            asset["group_name"] = group_names
            bulk_operations.append(
                UpdateOne({"_id": asset["_id"]}, {"$set": {"group_name": asset["group_name"]}})
            )

        if bulk_operations:
            result = mongo.db.assets.bulk_write(bulk_operations)
            logger.debug(f"Bulk write result: {result.bulk_api_result}")
            if result.modified_count > 0:
                return {"message": "Rules applied successfully"}, 200
            else:
                return {"message": "No rules were applied"}, 204
        else:
            return {"message": "No rules were applied"}, 204