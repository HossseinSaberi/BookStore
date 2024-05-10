import jwt
from datetime import datetime, timedelta
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, ParseError
from django.conf import settings
from django.contrib.auth import get_user_model, get_backends

User = get_user_model()

class AuthenticationService: 
    @classmethod
    def authenticate_user(cls, request,  username, password=None, has_password=True):
        backends = get_backends()
        for backend in backends:
            user = backend.authenticate(request=request, username=username, password=password, has_password=has_password)
            if user is not None:
                return user
        return None
       
    
class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        
        if jwt_token is None:
            return None

        jwt_token = self.get_the_token_from_header(jwt_token)
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=settings.JWT_CONF['ALGORITHM'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Has Expired!')
        except jwt.InvalidAlgorithmError:
            raise AuthenticationFailed('Invalid Token!')
        except:
            ParseError()

        user_identifier = payload.get('user_identifier')
        user = AuthenticationService.authenticate_user(request=request, username=user_identifier, has_password=False)
        return user, user.is_authenticated
    
    def authenticate_header(self, request):
        return settings.JWT_CONF['AUTH_HEADER']
    
    @classmethod
    def create_jwt(cls, user: User):
        payload = {
            'user_identifier': user.username,
            'exp': cls.get_exp_time(),
            'iat': datetime.now().timestamp(),
            'username': user.username,
            'phone_number': user.phone_number
        }
        
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_CONF['ALGORITHM'])
        return jwt_token
    
    def get_the_token_from_header(self, token):
        token = token.replace('Bearer', '').replace(' ', '')
        return token
    
    @classmethod
    def get_exp_time(cls):
        return int((datetime.now() + timedelta(hours=settings.JWT_CONF['TOKEN_LIFETIME_HOURS'])).timestamp())

