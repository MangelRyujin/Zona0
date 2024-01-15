from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from apps.orders.api.serializers.sendTransfer_serializer import TransferOSPSerializer
from rest_framework import status
from apps.users.models import User
from apps.orders.models import ReceiveOSP,TransferOSP
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# 'method' can be used to customize a single HTTP method of a view
receive_response = openapi.Response('response description', TransferOSPSerializer)
list_detail={
  "id": 0,
  "user": 0,
  "receive amount": 00.00,
  "receive user": 1,
  "date": "2024-01-09",
  "time": "string",
}

test_param = openapi.Parameter('code', openapi.IN_QUERY, description="enter an code", type=openapi.TYPE_STRING)
@swagger_auto_schema(method='post', manual_parameters=[test_param], responses={201: f'{list_detail}'})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def CreateTransferOSPView(request):
    user = get_object_or_404(User, pk=request.user.id)
    receive = get_object_or_404(ReceiveOSP, code=request.data['code'])
    if user.id != receive.user.id:
        if user.zona_point >= receive.amount:
            data = {'user': user.id, 'receive': receive.id}
            transfer_serializer = TransferOSPSerializer(data=data)
            if transfer_serializer.is_valid():
                transfer_serializer.save()
                return Response(transfer_serializer.data, status = status.HTTP_201_CREATED)
            else: return Response({'error':transfer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else: return Response({'error':f"No tienes {receive.amount} OSP para transferir"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':'No puedes pagarte a ti mismo'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='get', manual_parameters=None, responses={200: f'{list_detail}'})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ListSendTrasferOSPView(request):
    user = get_object_or_404(User, pk=request.user.id)
    if user:
        transfer = TransferOSP.objects.filter(user=user).order_by('-date', '-time')[:30]
        if transfer:
            transfer_serializer = TransferOSPSerializer(transfer, many=True)
            return Response(transfer_serializer.data, status = status.HTTP_200_OK)
        return Response({'message':'No se han realizado envios'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message':'Usuario no existe'}, status=status.HTTP_404_NOT_FOUND)