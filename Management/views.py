from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
from rest_framework import status
from .serializers import ObtainTokenSerializer
from .authentication import CustomJWTAuthentication, AuthenticationService
import jwt

# Create your views here.


class ObtainTokenView(APIView):
    # permission_classes = [AllowAny, ]
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = ObtainTokenSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception= True)
        user_identifier = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = AuthenticationService.authenticate_user(request=request, username=user_identifier, password=password)
        if not user:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        jwt_token = CustomJWTAuthentication.create_jwt(user)
        return Response({'token': jwt_token})

        