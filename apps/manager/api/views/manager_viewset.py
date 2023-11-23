from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from apps.orders.api.serializers.order_serializer import TransferManagerOrderSerializer,BurnManagerOrderSerializer
from rest_framework import status
from apps.users.models import Zona0Manager
from utils.send_email.send_email import send_email_transfer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_ZOP(request):
    
    manager = get_object_or_404(Zona0Manager, pk=request.user.id)
    user = get_object_or_404(get_user_model(), email=request.data['email'])
    if manager and user:
        data = {'cant_zona_point': request.data['cant_zona_point'], 'email': request.data['email'],'user_manager':request.user.id}
        transfer_serializer = TransferManagerOrderSerializer(data=data)
        if transfer_serializer.is_valid():
            send_email_transfer(request.user,request.data['email'],request.data['cant_zona_point'])
            transfer_serializer.save()
            serializer= transfer_serializer.data
            user.transfer_zop(serializer['cant_zona_point'])
            manager.recauder_zop(serializer['cant_zona_point'])
            return Response({'message':'Puntos enviados correctamente'}, status=status.HTTP_201_CREATED)
        else: return Response({'error':transfer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':'No tienes permiso para hacer la transferencia'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def burn_ZOP(request):
    
    manager = get_object_or_404(Zona0Manager, pk=request.user.id)
    user = get_object_or_404(get_user_model(), email=request.data['email'])
    if manager and user:
        data = {'cant_zona_point': request.data['cant_zona_point'], 'email': request.data['email'],'user_manager':request.user.id}
        transfer_serializer = BurnManagerOrderSerializer(data=data)
        if transfer_serializer.is_valid():
            transfer_serializer.save()
            serializer= transfer_serializer.data
            user.burn_zop(serializer['cant_zona_point'])
            manager.burn_zop(serializer['cant_zona_point'])
            return Response({'message':'Puntos quemados correctamente'}, status=status.HTTP_201_CREATED)
        else: return Response({'error':transfer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':'No tienes permiso para hacer la quema de puntos'}, status=status.HTTP_401_UNAUTHORIZED)
    