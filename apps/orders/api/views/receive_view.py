from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from apps.orders.api.serializers.transfer_serializer import ReceiveOSPSerializer, DetailReceiveOSPSerializer
from rest_framework import status
from apps.users.models import User
from apps.orders.models import ReceiveOSP
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# 'method' can be used to customize a single HTTP method of a view
receive_response = openapi.Response('response description', ReceiveOSPSerializer)
list_unpaid_receive={
  "id": 0,
  "user": 0,
  "amount": "string",
  "code": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "state": "Unpaid",
  "image": "string",
  "date": "2024-01-09",
  "time": "string"
}
list_paid_receive={
  "id": 0,
  "user": 0,
  "amount": "string",
  "code": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "state": "Paid",
  "image": "string",
  "date": "2024-01-09",
  "time": "string"
}

list_detail={
  "id": 0,
  "user": 0,
  "amount": "string",
  "code": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "state": "Unpaid",
  "date": "2024-01-09",
  "time": "string"
}


@swagger_auto_schema(method='get', manual_parameters=None, responses={200: f'{list_paid_receive}'})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListPaidReceiveOSPView(request):
    user = get_object_or_404(User, pk=request.user.id)
    receiver = ReceiveOSP.objects.filter(user=user).filter(state='Paid').order_by('-date', '-time')[:30]
    if receiver:
        transfer_serializer = ReceiveOSPSerializer(receiver, many=True)
        return Response(transfer_serializer.data, status = status.HTTP_200_OK)
    return Response({'message':'No existen recibos pagados'}, status=status.HTTP_404_NOT_FOUND)


test_param = openapi.Parameter('amount', openapi.IN_QUERY, description="enter an amount", type=openapi.TYPE_NUMBER)
@swagger_auto_schema(method='post', manual_parameters=[test_param], responses={201: receive_response})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def CreateReceiveOSPView(request):
    user = get_object_or_404(User, pk=request.user.id)
    if user:
        data = {'amount': request.data['amount'], 'user': request.user.id}
        transfer_serializer = ReceiveOSPSerializer(data=data)
        if transfer_serializer.is_valid():
            transfer_serializer.save()
            return Response(transfer_serializer.data, status = status.HTTP_201_CREATED)
        else: return Response({'error':transfer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':'Usuario no existe'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='get', manual_parameters=None, responses={200: f'{list_unpaid_receive}'})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ListUnpaidReceiveOSPView(request):
    user = get_object_or_404(User, pk=request.user.id)
    if user:
        receiver = ReceiveOSP.objects.filter(user=user).filter(state='Unpaid').order_by('-date', '-time')
        if receiver:
            transfer_serializer = ReceiveOSPSerializer(receiver, many=True)
            return Response(transfer_serializer.data, status = status.HTTP_200_OK)
        return Response({'message':'No existen solicitudes de recibos'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message':'Usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(method='post', manual_parameters=None, responses={200: f'{list_detail}'})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def DetailReceiveOSPView(request):
    receive = get_object_or_404(ReceiveOSP, code=request.data['code'])
    if receive :
        if receive.state == 'Unpaid':
            transfer_serializer = DetailReceiveOSPSerializer(receive)
            return Response(transfer_serializer.data, status = status.HTTP_200_OK)
        return Response({'message':'El recivo ya a sido pagado'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message':'No existe el recivo'}, status=status.HTTP_404_NOT_FOUND)




@swagger_auto_schema(method='delete', responses={200: 'Solicitud eliminada'})
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def DeleteUnpaidReceiveOSPView(request,id):
    user = get_object_or_404(User, pk=request.user.id)
    if user:
        receiver = ReceiveOSP.objects.filter(pk=id).filter(user=user).filter(state='Unpaid').first()
        if receiver:
            receiver.delete()
            return Response({'message':'Solicitud eliminada'}, status = status.HTTP_200_OK)
        return Response({'message':'No existe esa solicitud'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message':'Usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
