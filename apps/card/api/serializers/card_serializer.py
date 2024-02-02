from django.core.exceptions import ValidationError
from rest_framework import serializers
from apps.card.models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id','user','min_withdraw','active','discount_code')
        
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user' : instance.user.username,
            'min_withdraw': instance.min_withdraw,
            'active' : instance.active,
            'discount_code' : instance.discount_code,
        }
        
class Discount_CodeCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('discount_code')
        
    def to_representation(self, instance):
        return {
            'discount_code' : instance.discount_code,
        }

class Min_WithdrawCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id','min_withdraw','active','discount_code')
        
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'min_withdraw': instance.min_withdraw,
            'active' : instance.active,
            'discount_code' : instance.discount_code,
            
        }
        
    def min_withdraw_validation(value):
        if value >= 0:
            return value
        else: 
            raise ValidationError("El valor debe ser mayor que 0")
        
    
