from rest_framework import serializers
from apps.orders.models import ReceiveOSP
from django.core.exceptions import ValidationError
import qrcode
from PIL import Image   



class ReceiveOSPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiveOSP
        fields = ('id','user','amount','code','state','image','date','time')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['image']:
            url = representation['image']
            url_image = url.split("&export=download")[0]
            representation['image'] = url_image
        return {
            'id':instance.id,
            'user':instance.user.username,
            'code':instance.code,
            'state':instance.state,
            'amount':instance.amount,
            'image':url_image,
            'date': instance.date,
            'time': instance.time,
        }
        
    def validate_amount(self,data):
        if data > 0:
            return data
        else: 
            raise ValidationError("Debes de recibir un valor mayor a 0.")
    

class CreateReceiveOSPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiveOSP
        fields = ('id','user', 'state', 'amount', 'code', 'image')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        url = representation['image']
        url_image = url.split("&export=download")[0]
        return {
            'id':instance.id,
            'user':instance.user.username,
            'code':instance.code,
            'state':instance.state,
            'amount':instance.amount,
            'image':url_image,
        }  
        
class DetailReceiveOSPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiveOSP
        fields = ('id','user', 'state', 'amount', 'code','date','time')
        
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'user':instance.user.username,
            'code':instance.code,
            'state':instance.state,
            'amount':instance.amount,
            'date': instance.date,
            'time': instance.time,
        }  
        
    