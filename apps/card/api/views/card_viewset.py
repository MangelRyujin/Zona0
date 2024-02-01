from rest_framework.response import Response
import rest_framework
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.users.models import User
from decimal import Decimal
from rest_framework.decorators import action
from apps.card.api.serializers.card_serializer import CardSerializer, Discount_CodeCardSerializer,Min_WithdrawCardSerializer
from apps.card.models import Card


class CardViewSet(viewsets.GenericViewSet):
    serializer_class= CardSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self,user=None):
        if user is None:
            return None
        return self.get_serializer().Meta.model.objects.filter(user = user).filter(on_hold = False).first()
    
    
    def list(self, request):
        card = self.get_queryset(request.user.id)
        if card:
            card_serializers = self.serializer_class(card)
            return Response(card_serializers.data, status= status.HTTP_200_OK)
        return Response({'message':'No existe la tarjeta'}, status= status.HTTP_404_NOT_FOUND)
    
    
    @action(detail = False, methods = ['put'])
    def change_discount_code(self,request):
        card = Card.objects.filter(on_hold = False).filter(id=request.query_params.get('id')).filter(user= request.user.id).first()
        if card:
            card.save()
            serializers = Discount_CodeCardSerializer(card)
            return Response(serializers.data, status = status.HTTP_200_OK)
        return Response({'error':f'Tarjeta no encontrada'}, status= status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail = False, methods = ['put'])
    def min_withdraw_code(self,request):
        card = Card.objects.filter(on_hold = False).filter(id=request.query_params.get('id')).filter(user= request.user.id).first()
        if card:
            data = {'min_withdraw':request.data['min_withdraw'], 'active':card.active, 'discount_code':card.discount_code}
            serializers = Min_WithdrawCardSerializer(card,data = data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status = status.HTTP_200_OK)
            return Response(serializers.errors, status= status.HTTP_400_BAD_REQUEST)
        return Response({'error':f'Tarjeta no encontrada'}, status= status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail = False, methods = ['put'])
    def active_code(self,request):
        card = Card.objects.filter(on_hold = False).filter(id=request.query_params.get('id')).filter(user= request.user.id).first()
        if card:
            card.active = True
            card.save()
            serializers = self.serializer_class(card)
            return Response(serializers.data, status = status.HTTP_200_OK)
        return Response({'error':f'Tarjeta no encontrada'}, status= status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail = False, methods = ['put'])
    def desactive_code(self,request):
        card = Card.objects.filter(on_hold = False).filter(id=request.query_params.get('id')).filter(user= request.user.id).first()
        if card:
            card.active = False
            card.save()
            serializers = self.serializer_class(card)
            return Response(serializers.data, status = status.HTTP_200_OK)
        return Response({'error':f'Tarjeta no encontrada'}, status= status.HTTP_400_BAD_REQUEST)