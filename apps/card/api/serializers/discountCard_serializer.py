from decimal import Decimal
from django.core.exceptions import ValidationError
from rest_framework import serializers
from apps.card.models import DiscountCard


class DiscountCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCard
        fields = ('id','card','user','amount','date','time')
        
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'card_user' : instance.card.user.username,
            'user': instance.user.username,
            'amount' : instance.amount,
            'date': instance.date,
            'time' : instance.time,
        }
        
    def validate_amount(self,data):
        try:
            data = Decimal(data)
        except ValueError:
            raise ValidationError("El valor debe ser un número decimal.")
        if data <= 0: 
            raise ValidationError("El valor debe ser mayor que 0")
        if self.context['user'].zona_point < data: 
            raise ValidationError("No contienes esa cantidad")

        return data