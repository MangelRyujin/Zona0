from rest_framework import serializers
from apps.orders.models import TransferOSP,ReceiveOSP
from django.core.exceptions import ValidationError
from apps.manager.api.views.manager_viewset import send_ZOP
 


class ReceiveOSPSerializer(serializers.ModelSerializer):
    class Meta:
       model = ReceiveOSP
       fields = ('id','user', 'state', 'amount', 'code','date','time')
       
    def to_representation(self, instance):
        
        return {
            'id':instance.id,
            'user':instance.user,
            'state':instance.state,
            'code':instance.code,
            'amount':instance.amount,
            'date':instance.date,
            'time':instance.time,
        }


class TransferOSPSerializer(serializers.ModelSerializer):
    # receive = ReceiveOSPSerializer()
    class Meta:
        model = TransferOSP
        fields = ('id','user','receive','date','time')
        
    def to_representation(self, instance):
        
        return {
            'id':instance.id,
            'user':instance.user.username,
            'receive amount':instance.receive.amount,
            'receive user':instance.receive.user.username,
            'date':instance.date,
            'time':instance.time,
        }
    
    def create(self, validated_data):
        transfer = TransferOSP.objects.create(**validated_data)
        validated_data['user'].burn_zop(validated_data['receive'].amount)
        validated_data['receive'].user.transfer_zop(validated_data['receive'].amount)
        validated_data['receive'].state_Paid()
        return transfer
         
        
    