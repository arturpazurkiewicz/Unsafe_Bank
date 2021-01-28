from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.response import Response

from www_bank.models import *
from www_bank.serializers import TransferSerializer


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
        serializer = TransferSerializer(TransferHistory.objects.filter(account_id=account))
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAdminUser,))
def show_full_transaction(request):
    serializer = TransferSerializer(TransferHistory.objects.all())
    return Response(serializer.data, status=status.HTTP_200_OK)


