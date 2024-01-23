from django.core.exceptions import ValidationError
from rest_framework import serializers
from apps.banking.models import Banking


class BankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banking
        fields = ('id','user','amount','date','time')
        
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user' : instance.user.username,
            'amount' : instance.amount,
            'date' : instance.date,
            'time' : instance.time,
        }
        
    def validate_amount(self,data):
        if data > 0:
            if self.context['user'].zona_point >= data:
                return data
            else:
                raise ValidationError("No contiene esa cantidad")
        else:
            raise ValidationError("Debe de bancarizar una suma mayor que 0")
    
