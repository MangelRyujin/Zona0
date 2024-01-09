from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from apps.orders.api.serializers.transfer_serializer import ReceiveOSPSerializer
from rest_framework import status
from apps.users.models import User
from apps.orders.models import ReceiveOSP
from utils.send_email.send_email import send_email_transfer


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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ListPaidReceiveOSPView(request):
    user = get_object_or_404(User, pk=request.user.id)
    receiver = ReceiveOSP.objects.filter(user=user).filter(state='Paid').order_by('-date', '-time')[:30]
    if receiver:
        transfer_serializer = ReceiveOSPSerializer(receiver, many=True)
        return Response(transfer_serializer.data, status = status.HTTP_200_OK)
    return Response({'message':'No existen recibos pagados'}, status=status.HTTP_404_NOT_FOUND)
  
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ListUnpaidReceiveOSPView(request):
    user = get_object_or_404(User, pk=request.user.id)
    if user:
        receiver = ReceiveOSP.objects.filter(user=user).filter(state='Unpaid').order_by('-date', '-time')[:30]
        if receiver:
            transfer_serializer = ReceiveOSPSerializer(receiver, many=True)
            return Response(transfer_serializer.data, status = status.HTTP_200_OK)
        return Response({'message':'No existen solicitudes de recibos'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'message':'Usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

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
