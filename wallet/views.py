from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status 
from .models import Wallet
from .serializers import WalletSerializer, FundWalletSerializer
from rest_framework.permissions import IsAdminUser


"""
This endpoint gets all the wallet object for each user.
"""
@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_wallets(request):
    if request.method == "GET":
        try:
            user_wallets = Wallet.objects.all()
            serialized_user_wallets = WalletSerializer(user_wallets, many=True)

            return Response(serialized_user_wallets.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": f"The error {e} has occurred"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)

"""
This endpoint handles the display of each individual wallet, provided the user id is passed in the url as well.
"""
@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_wallet_view(request, id):
    if request.method == "GET":
        try:
            user_wallet = Wallet.objects.get(id=id)
            serialized_user_wallet = WalletSerializer(user_wallet)

            return Response(serialized_user_wallet.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": f"The error {e} occured"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)
    
"""
This endpoint handles the funding of single wallets, providing the user id of the wallet you want to fund
"""
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def fund_single_wallet(request, id):
    if request.method == "PATCH":
        try: 
            user = User.objects.get(id=id)
            update_wallet = FundWalletSerializer(user, data=request.data, partial=True)
            if update_wallet.is_valid():
                update_wallet.save()

                return Response({"Message": f"New Wallet Balance is {update_wallet.data.get('balance')}"}, status=status.HTTP_200_OK)
            else:
                return Response(update_wallet.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Error": f"The error {e} has occured"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)


"""
This endpoint handles bulk wallet funding, i.e funding all user wallets
"""
@api_view(['PATCH'])
def fund_all_wallet(request):
    if request.method == "PATCH":
        try:
            users = User.objects.all()
            for user in users:
                update_multiple_wallets = FundWalletSerializer(user, data=request.data, many=isinstance(request.data, list))
                if update_multiple_wallets.is_valid():
                    update_multiple_wallets.save()
            return Response({f"All users wallets have been updated to {update_multiple_wallets.data.get('balance')}"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": f"An error {e} has occured"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invalid request type"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def delete_all_wallets(request):
    if request.method == 'GET':
        try:
            all_wallets = Wallet.objects.all()
            all_wallets.delete()

            return Response({"Message": "All wallets have been deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": f"The error {e} occured"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Error": "Invallid request type"}, status=status.HTTP_400_BAD_REQUEST)
    


