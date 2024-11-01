from marshmallow import Schema, fields

class UserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    description = fields.String()
