from marshmallow import Schema, fields, validate


class AuthSchema(Schema):

    login = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100, error="O nome de usuário deve ter entre 1 e 100 caracteres.")
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=255, error="A senha deve ter entre 6 e 255 caracteres.")
    )
