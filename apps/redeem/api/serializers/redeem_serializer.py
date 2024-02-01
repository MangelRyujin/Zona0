from rest_framework import serializers
from apps.redeem.models import MarketingApplican,Code
from django.core.exceptions import ValidationError


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ('id','marketingApplican','prize_fund','code','redeem')
        
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'marketingApplican':instance.marketingApplican.place,
            'prize_fund':instance.prize_fund,
            'code':instance.code,
            'redeem': instance.redeem,

        }
        
    

class MarketingApplicanSerializer(serializers.ModelSerializer):
    marketingApplican = CodeSerializer(many = True, read_only=True)
    class Meta:
        model = MarketingApplican
        fields = ('id','place','prize_fund','winners','cant_codes','date','time','marketingApplican')
        
        
    def validate_prize_fund(self,data):
        
        if data > 0:
            return data
        else: 
            raise ValidationError("El monto es incorrecto")
    
    def validate_winners(self,data):

        if data > 0:
            return data
        else: 
            raise ValidationError("Al menos debes de introducir un ganador")
        
    def validate_cant_codes(self,data):
     
        if data > 0:
            return data
        else: 
            raise ValidationError("Al menos debes de introducir un ganador")   
    
