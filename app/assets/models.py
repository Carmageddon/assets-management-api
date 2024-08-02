from marshmallow import Schema, fields

class TagSchema(Schema):
    key = fields.Str(required=True)
    value = fields.Str(required=True)

class CloudAccountSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)

class AssetSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    tags = fields.List(fields.Nested(TagSchema), required=False)
    cloud_account = fields.Nested(CloudAccountSchema, required=True)
    owner_id = fields.Str(required=True)
    region = fields.Str(required=False)
    group_name = fields.Str(required=False)
