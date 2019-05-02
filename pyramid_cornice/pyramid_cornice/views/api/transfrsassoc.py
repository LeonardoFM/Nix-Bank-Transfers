from cornice import Service
from cornice.validators import marshmallow_body_validator
from pyramid_cornice.views.api.schema import CrientSchema

transfer_assoc = Service(name='transfers',path='apt/v1/transfers')
#
# Cornice is a REST but must response treatment: status code
# this is done with seralization schema
@transfer_assoc.post(schema=CrientSchema,
                     validators=(marshmallow_body_validator,),
                     content_type='aplication/json')
def create_transfer_assoc(request):
    return {}
