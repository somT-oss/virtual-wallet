from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from wallet.models import Wallet
from wallet.serializers import WalletSerializer

""""
This endpoint handles registering of employees, only by the admin.
"""
@swagger_auto_schema(method='POST', request_body=UserRegistrationSerializer)
@api_view(['POST'])
def register_employee(request):
    if request.method == "POST":
        register_serializer = UserRegistrationSerializer(data=request.data)
        if register_serializer.is_valid():
            user_email = register_serializer.validated_data.get('email')
            all_emails = User.objects.all().values_list('email', flat=True)
            if user_email in all_emails:
                return Response({"Error": "This email is already in use"}, status=status.HTTP_400_BAD_REQUEST)
            user_username = register_serializer.validated_data.get('username')
            all_usernames = User.objects.values_list('username', flat=True)
            if user_username in all_usernames:
                return Response({"Error": "This username is already in use"}, status=status.HTTP_400_BAD_REQUEST)
            register_serializer.save()
            message = {
                "id": register_serializer.data.get('id'),
                "username": register_serializer.data.get('username'),
                "first_name": register_serializer.data.get('first_name'),
                "last_name": register_serializer.data.get('last_name'),
                "email": register_serializer.data.get('email')
            }
            return Response(message, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error": register_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invalid request type"})


@swagger_auto_schema(method='POST', request_body=UserRegistrationSerializer)
@api_view(['POST'])
def create_admin_user(request):
    if request.method == 'POST':
        superuser_serializer = UserRegistrationSerializer(data=request.data)
        if superuser_serializer.is_valid():
            
            """
            Checks if an email already exists in the database.
            """
            
            user_email = superuser_serializer.validated_data.get('email')
            all_emails = User.objects.all().values_list('email', flat=True)
            if user_email in all_emails:
                return Response({"Error": "This email is already in use"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            """
            Checks if a username already exists in the database.
            """
            
            user_username = superuser_serializer.validated_data.get('username')
            all_usernames = User.objects.values_list('username', flat=True)
            if user_username in all_usernames:
                return Response({"Error": "This username is already in use"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            username = superuser_serializer.data.get('username')
            email = superuser_serializer.data.get('email')
            password = superuser_serializer.data.get('password')
            first_name = superuser_serializer.data.get('first_name')
            last_name = superuser_serializer.data.get('last_name')

            superuser = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, is_superuser=True, is_staff=True)
            superuser.save()
            message = {
                "id": superuser_serializer.data.get('id'),
                "username": superuser_serializer.data.get('username'),
                "first_name":superuser_serializer.data.get('first_name'),
                "last_name": superuser_serializer.data.get('last_name'),
                "email": superuser_serializer.data.get('email')
            }
            return Response({"Message": "Superuser has been created", "Details": message}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error": superuser_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "You're using the wrong request type"})

"""
This endpoint handles login in of created employees by the admin.
"""

@swagger_auto_schema(method='POST', request_body=UserLoginSerializer)
@api_view(['POST'])
def login_employee(request):
    if request.method == 'POST':
        user_serializer = UserLoginSerializer(data=request.data)
        if user_serializer.is_valid():
            try:
                user_email = user_serializer.data.get("email")
                user = User.objects.get(email=user_email)
                refresh = RefreshToken.for_user(user)
                return Response ({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            except Exception:
                return Response({"Error": f"Sorry, user with email {user_email} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)

"""
This endpoint handle returning of individual users with their firstname passed as a parameter in the url
"""

@swagger_auto_schema(method='GET')
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=id)
            serialized_user = UserRegistrationSerializer(user)
            user_wallet = Wallet.objects.get(user=user.id)
            serialized_user_wallet = WalletSerializer(user_wallet)

            message = {
                "first_name": serialized_user.data.get('first_name'),
                "last_name": serialized_user.data.get('last_name'),
                "balance": serialized_user_wallet.data.get('balance')
            }
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": f"The user with id {id} does not exist"})
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)

"""
This endpoint handles updating user information of individual users by passing the firstname as a parameter in the url
"""

@swagger_auto_schema(method='PATCH', request_body=UserUpdateSerializer)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request, id):
    if request.user.id == id:
        update_serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if update_serializer.is_valid():
            update_serializer.save()
            message =  {
                "first_name": update_serializer.data.get('first_name'),
                "last_name": update_serializer.data.get('last_name'),
                "email": update_serializer.data.get('email')
            }
            return Response({"Update Message": message}, status=status.HTTP_200_OK)
        else:
            return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "You don't have perimissions to edit this users info"}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='POST')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_all_users(request):
    if request.method == 'GET':
        try:
            all_users = User.objects.all()
            all_users.delete()

            return Response({"Message": "All users have been deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": f"The error {e} occured"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invallid request type"}, status=status.HTTP_400_BAD_REQUEST)