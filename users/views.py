from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


""""
This endpoint handles registering of employees, only by the admin.
"""
@api_view(['POST'])
def register_employee(request):
    if request.method == "POST":
        register_serializer = UserRegistrationSerializer(data=request.data)
        if register_serializer.is_valid():
            register_serializer.save()

            return Response({"Success": f"Employee Account Created for {register_serializer.data.get('first_name')} {register_serializer.data.get('last_name')}"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error": register_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invalid request type"})

@api_view(['POST'])
def create_admin_user(request):
    if request.method == 'POST':
        superuser_serializer = UserRegistrationSerializer(data=request.data)
        if superuser_serializer.is_valid():
            username = superuser_serializer.data.get('username')
            email = superuser_serializer.data.get('email')
            password = superuser_serializer.data.get('password')
            first_name = superuser_serializer.data.get('first_name')
            last_name = superuser_serializer.data.get('last_name')

            superuser = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, is_superuser=True, is_staff=True)
            superuser.save()
            return Response({"Message": "Superuser has been created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error": superuser_serializer.erros}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "You're using the wrong request type"})

"""
This endpoint handles login in of created employees by the admin.
"""
@api_view(['POST'])
def login_employee(request):
    if request.method == 'POST':
        user_serializer = UserLoginSerializer(data=request.data)
        if user_serializer.is_valid():
            user_email = user_serializer.data.get("email")
            user = User.objects.get(email=user_email)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response ({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"Error": f"User with {user_email} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)

"""
This endpoint handle returning of individual users with their firstname passed as a parameter in the url
"""
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, firstname):
    if request.method == 'GET':
        user = User.objects.get(first_name=firstname)
        serialized_user = UserRegistrationSerializer(user)

        return Response({"Message": f"Hello {serialized_user.data.get('first_name')} {serialized_user.data.get('last_name')}"}, status=status.HTTP_200_OK)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)

"""
This endpoint handles updating user information of individual users by passing the firstname as a parameter in the url
"""
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request, firstname):
    if request.user.first_name == firstname:
        update_serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if update_serializer.is_valid():
            update_serializer.save()

            return Response({"Message": "User data has been updated"}, status=status.HTTP_200_OK)
        else:
            return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "You don't have perimissions to edit this users info"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
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