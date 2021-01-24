import os
import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "Not set")
ALGORITHMS = os.getenv("ALGORITHMS", "Not set")
API_AUDIENCE = os.getenv("API_AUDIENCE", "Not set")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "Not set")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "Not set")

if AUTH0_DOMAIN == "Not set":
    #not AUTH0_DOMAIN or not ALGORITHMS or notAPI_AUDIENCE or not AUTH0_CLIENT_ID or not AUTH0_CALLBACK_URL:
    print("no environment detected. takes preset")
    AUTH0_DOMAIN= os.getenv('AUTH0_DOMAIN',"dev-t-4sg5-6.eu.auth0.com")
    API_AUDIENCE=os.getenv("API_AUDIENCE","agency")
    ALGORITHMS=os.getenv("ALGORITHMS",['RS256'])
    AUTH0_CLIENT_ID=os.getenv("AUTH0_CLIENT_ID","DRQkvwQZrdvpBOs65wzGSz4pmxTps1tx")
    AUTH0_CALLBACK_URL=os.getenv("AUTH0_CALLBACK_URL","https://localhost:5000")



## AuthError Exception

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

## Auth Header

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

def check_permissions(permission, payload):
    if 'permissions' not in payload:
                        raise AuthError({
                            'code': 'invalid_claims',
                            'description': 'Permissions not included in JWT.'
                        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True


def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    
    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.',
            'error': 401,
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'success': False,
                'code': 'token_expired',
                'description': 'Token expired.',
                'error': 401,
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'success': False,
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.',
                'error': 401,
            }, 401)
        
        except Exception:
            raise AuthError({
                'success': False,
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.',
                'error': 400
            }, 400)
    
    raise AuthError({
                'success': False,
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.',
                'error': 400
            }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator