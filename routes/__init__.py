from flask_restx import Api

from .users import api as ns1

authorizations = {
    'jwt' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'Authorization'
    }
}

api = Api(
    title='My Title',
    authorizations=authorizations,
    version='1.0',
    description='A description',
    # All API metadatas
)


api.add_namespace(ns1)