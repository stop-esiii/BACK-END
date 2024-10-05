from marshmallow import Schema, fields, validate


class UserSchemaPOST(Schema):

    id_type_role = fields.Int(
        required=True, 
        validate=validate.Range(min=1, max=4, error="id_type_role inexistente.")
    )
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100, error="O nome de usuário deve ter entre 1 e 100 caracteres.")
    )
    email = fields.Str(
        required=True, 
        validate=validate.Length(max=100, error="O email não deve exceder 100 caracteres.")
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=255, error="A senha deve ter entre 6 e 255 caracteres.")
    )
    image = fields.Str(
        validate=validate.Length(max=65535, error="Os dados da imagem não devem exceder 65535 caracteres.")
    )

class UserSchemaGET(Schema):

    id = fields.Int()
    id_type_role = fields.Int()
    username = fields.Str()
    email = fields.Str()
    image = fields.Str()
    dt_insert = fields.DateTime()
    dt_update = fields.DateTime()
    themes = fields.Str()

class UserSchemaPUT(Schema):

    id_type_role = fields.Int(
        validate=validate.Range(min=1, max=4, error="id_type_role inexistente.")
    )
    username = fields.Str(
        validate=validate.Length(min=1, max=100, error="O nome de usuário deve ter entre 1 e 100 caracteres.")
    )
    email = fields.Str(
        validate=validate.Length(max=100, error="O email não deve exceder 100 caracteres.")
    )
    image = fields.Str(
        validate=validate.Length(max=65535, error="Os dados da imagem não devem exceder 65535 caracteres.")
    )
    themes = fields.Str(
        validate=validate.Length(max=65535, error="Os dados dos temas não devem exceder 65535 caracteres.")
    )
