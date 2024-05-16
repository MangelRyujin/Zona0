from django.core.exceptions import ValidationError
from rest_framework import serializers
from apps.banking.models import Banking


class BankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banking
        fields = ('id','user','state','amount','date','time','interest','date_banked','post_interest')
        
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user' : instance.user.username,
            'amount' : instance.amount,
            'state': instance.state,
            'date' : instance.date,
            'time' : instance.time,
            'interest':instance.interest(),
            'post_interest':instance.post_interest(),
            'date_banked':instance.date_banked(),
            
            
        }
        
    def validate_amount(self,data):
        if data > 0:
            if self.context['user'].zona_point >= data:
                return data
            else:
                raise ValidationError("No contiene esa cantidad")
        else:
            raise ValidationError("Debe de bancarizar una suma mayor que 0")
    
