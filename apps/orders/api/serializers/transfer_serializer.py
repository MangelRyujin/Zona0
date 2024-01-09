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
        
        
    # def create(self, validated_data):
    #     receive = ReceiveOSP.objects.create(**validated_data)
    #     # Create qrcode
    #     qr = qrcode.make(f'{receive.code}')
    #     if qr:
    #         receive.image = qr.save(f'{receive.id}.png')
        
    #     receive.save()
    #     print('recivo')
    #     print(receive)
    #     print('creado')
    #     return receive

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
        
    