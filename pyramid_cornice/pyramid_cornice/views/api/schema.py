from marshmallow import Schema, fields, validate
# serialization schema
class CrientSchema(Schema):
    nome = fields.String(required=True, validate=validate.Length(min=2,max=255))
    cnpj = fields.Integer(required=True)

class TransferSchema(Schema):
    Transfers = fields.Nested
