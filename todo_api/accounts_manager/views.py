from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from django.utils.crypto import get_random_string
from django.core.mail import send_mail

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


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print('User not found.')
            return Response({'error': 'User Does not exists'}, status=status.HTTP_404_NOT_FOUND)

        # Generate unique token and save to database
        token = get_random_string(length=32)
        user.password_reset_token = token
        user.save()

        # Send password reset email
        reset_url = f'http://localhost:3000/reset-password/{token}/'
        send_mail(
            'Reset your password',
            f'Hi, here is the link to reset your password: {reset_url}',
            '',
            [email],
            fail_silently=False,
        )

        return Response({'success': 'An email will be sent to your email address'}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    def post(self, request, token):
        try:
            user = User.objects.get(password_reset_token=token)
        except User.DoesNotExist :
            return Response({'error': 'User Does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Update user password
        user.set_password(request.data['password'])
        user.password_reset_token = None
        user.save()

        return Response({'success': 'Password reset successfully'}, status=status.HTTP_200_OK)


