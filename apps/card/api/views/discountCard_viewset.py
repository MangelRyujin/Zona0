from rest_framework.response import Response
import rest_framework
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.card.models import Card,DiscountCard
from apps.users.models import User
from decimal import Decimal
from rest_framework.decorators import action
from django.utils import timezone
from apps.card.api.serializers.discountCard_serializer import DiscountCardSerializer


class DiscountCardViewSet(viewsets.GenericViewSet):
    serializer_class= DiscountCardSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self,pk=None,user=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(user = user).order_by('-date', '-time')[:20]
        return self.get_serializer().Meta.model.objects.filter(user = user).filter(pk = pk).first()
    
    
    def list(self, request):
        card = self.get_queryset(None,request.user.id)
        if card.exists():
            card_serializers = self.serializer_class(card,many=True)
            return Response(card_serializers.data, status= status.HTTP_200_OK)
        return Response({'message':'No existen descuentos'}, status= status.HTTP_404_NOT_FOUND)
    
    
    def retrieve(self, request,pk=None):
        card = self.get_queryset(pk,request.user.id)
        if card:
            card_serializers = self.serializer_class(card)
            return Response(card_serializers.data, status= status.HTTP_200_OK)
        return Response({'message':'No existe el descuento'}, status= status.HTTP_404_NOT_FOUND)
    
    
    def create(self,request):
        user = get_object_or_404(User, pk = request.user.id)
        card = Card.objects.filter(pin=request.query_params.get('pin')).filter(active=True).filter(on_hold=False).first()
        if card:
            if card.user != request.user:
                discounts = DiscountCard.objects.filter(card=card.id).filter(date=timezone.now().date())
                min = 0
                for discount in discounts:
                    min+=discount.amount
                if card.min_withdraw-Decimal(min) >= Decimal(request.data['amount']):
                    data = {'card':card.id,'user':request.user.id, 'amount':Decimal(request.data['amount'])}
                    serializers = self.serializer_class(data = data, context={'user':card.user})
                    if serializers.is_valid():
                        serializers.save()
                        user.transfer_zop(Decimal(request.data['amount']))
                        user.save()
                        card.user.burn_zop(Decimal(request.data['amount']))
                        card.user.save()
                        card.save()
                        return Response(serializers.data, status = status.HTTP_201_CREATED)
                    return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)
                return Response({'error':f"Lo sentimos excede el máximo de descuento diario de esa tarjeta, máximo a extraer {card.min_withdraw-Decimal(min)}"},status = status.HTTP_400_BAD_REQUEST)
            return Response({'error':'No puede descontarce a usted mismo'},status = status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Tarjeta no existente'}, status= status.HTTP_404_NOT_FOUND)
    
    
class YourDiscountCardViewSet(viewsets.GenericViewSet):
    serializer_class= DiscountCardSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self,pk=None,card=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(card = card).order_by('-date', '-time')[:20]
        return self.get_serializer().Meta.model.objects.filter(card = card).filter(pk = pk).first()
    
    
    def list(self, request):
        card = get_object_or_404(Card,user = request.user.id)
        print( request.user)
        discount = self.get_queryset(None,card.id)
        if discount.exists():
            discount_serializers = self.serializer_class(discount,many=True)
            return Response(discount_serializers.data, status= status.HTTP_200_OK)
        return Response({'message':'No existen descuentos'}, status= status.HTTP_404_NOT_FOUND)
    
    
    def retrieve(self, request,pk=None):
        card = get_object_or_404(Card,user = request.user.id)
        discount = self.get_queryset(pk,card.id)
        if discount:
            discount_serializers = self.serializer_class(discount)
            return Response(discount_serializers.data, status= status.HTTP_200_OK)
        return Response({'message':'No existe el descuento'}, status= status.HTTP_404_NOT_FOUND)
    

