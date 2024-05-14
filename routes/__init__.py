from flask_restx import Api

from .users import api as ns1
from .auth import api as ns2

authorizations = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'jwtrefresh': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
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
api.add_namespace(ns2)