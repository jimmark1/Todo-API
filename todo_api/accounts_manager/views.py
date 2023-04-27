from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from . serializers import UserManagerSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(APIView):
    
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
       try:
              data = request.data['formData']

              name = data['name']
              email = data['email']
              username = data['username']
              password = data['password']
              re_password = data['re_password']

              if password == re_password:
                     if len(password) >= 8:
                            if not User.objects.filter(username=username).exists():
                                   user = User.objects.create_user(
                                          name=name,
                                          email=email,
                                          username=username,
                                          password=password
                                          
                                   )
                                   user.save()
                                   return Response({'success' :'User account created successfully'},
                                                 status=status.HTTP_201_CREATED
                                                 )
                            else:
                                   return Response(
                                   {'error' : 'Username already exists'},
                                   status=status.HTTP_400_BAD_REQUEST)        
                     else:
                            return Response(
                                   {'error' : 'Password must be atleast 8 characters'},
                                   status=status.HTTP_400_BAD_REQUEST
                                   )                           
              else:
                     return Response(
                           {'error' : 'Passwords do not match'},
                           status=status.HTTP_400_BAD_REQUEST
                           )
           
       except Exception as e:
              return Response(
                     {'error' : 'Something went wrong when creating an account'}, 
                     status=status.HTTP_500_INTERNAL_SERVER_ERROR
                     )
              
class RetrieveUserView(APIView):
      
      def get(self, request, format=None):
           
              try:
                     user = request.user
                     user = UserManagerSerializer(user)

                     return Response({'User' : user.data},
                                   status=status.HTTP_200_OK
                                   )
              except:
                     return Response(
                     {'error' : 'Something went wrong when retrieving user details'}, 
                     status=status.HTTP_500_INTERNAL_SERVER_ERROR
                     )

#JWT CUSTOMIZED TOKEN CLAIMS
class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.name
        token['is_active'] = user.is_active
        token['is_superuser'] = user.is_superuser
        return token

class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    
