from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.response import Response

from www_bank.forms import SignUpForm
from www_bank.models import *
from www_bank.serializers import TransferSerializer, AccountSerializer, FullUserSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_transaction(request, transaction_id):
    try:
        serializer = TransferSerializer(
            TransferHistory.objects.get(id=transaction_id, account_id__user_id=request.user), many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_all_transactions(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user_id=request.user)
        serializer = TransferSerializer(TransferHistory.objects.filter(account_id=account), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def show_full_transaction(request):
    serializer = TransferSerializer(TransferHistory.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def show_account(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user_id=request.user)
        serializer = AccountSerializer(account, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def delete_transaction(request, transaction_id):
    try:
        transaction = TransferHistory.objects.get(id=transaction_id, is_accepted=False)
        transaction.delete()
        return Response("Deleted", status=status.HTTP_200_OK)
    except:
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def accept_transaction(request, transaction_id):
    try:
        transaction = TransferHistory.objects.get(id=transaction_id)
        transaction.is_accepted = True
        transaction.save()
        return Response("Accepted", status=status.HTTP_200_OK)
    except:
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    serialized = FullUserSerializer(data=request.data)
    if serialized.is_valid():
        user = serialized.save()
        user.set_password(user.password)
        user.save()
        return Response("Created", status=status.HTTP_201_CREATED)
    else:
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
