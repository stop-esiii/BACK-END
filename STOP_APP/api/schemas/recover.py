from marshmallow import Schema, fields, validate


class RecoverSchemaPOST(Schema):

    email = fields.Str(
        required=True,
        validate=validate.Length(max=100, error="O email não deve exceder 100 caracteres.")
    )

class RecoverSchemaPUT(Schema):

    verification_code = fields.Str(
        required=True,
        validate=validate.Length(min=9, max=9, error="Código de verificação inválido.")
    )
    email = fields.Str(
        required=True,
        validate=validate.Length(max=100, error="O email não deve exceder 100 caracteres.")
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=255, error="A senha deve ter entre 6 e 255 caracteres.")
    )
