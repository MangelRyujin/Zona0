from rest_framework import serializers
from apps.orders.models import TransferOrderUsers, TransferManagerOrderUsers
from django.core.exceptions import ValidationError
from apps.users.models import User,Zona0Manager
        
class TransferOrderUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferOrderUsers
        fields = ('id','user','email','cant_zona_point','date','time')
        
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'user':instance.user.username,
            'email':instance.email,
            'cant_zona_point':instance.cant_zona_point,
            'date': instance.date,
            'time': instance.time,
        }
        
    def validate_email(self,data):
        user = User.objects.filter(email=data).first()
        if user and user.email == data:
            return data
        else:
            raise ValidationError("El usuario al que desea enviar la transferencia no existe.")
    
    def validate_cant_zona_point(self,data):
        user = User.objects.filter(id=self.initial_data['user']).first()
        if user:
            if data > 0 and user.zona_point - data > 0:
                return data
            else: raise ValidationError("No puedes extraer esa cantidad.")
        else:
            raise ValidationError("El usuario no existe.")
        
    
    def create(self, validated_data):
        order = TransferOrderUsers.objects.create(**validated_data)
        return order
    
class TransferManagerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferManagerOrderUsers
        fields = ('id','user_manager','email','type','cant_zona_point','date','time')
        
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'user_manager':instance.user_manager.username,
            'email':instance.email,
            'type':instance.type,
            'cant_zona_point':instance.cant_zona_point,
            'date': instance.date,
            'time': instance.time,
        }
        
    def validate_email(self,data):
        user = User.objects.filter(email=data).first()
        manager = Zona0Manager.objects.filter(email=data).first()
        if manager:
            raise ValidationError("No puedes realizar una transferencia a un manager.")  
        else:
            if user and user.email == data:
                return data
            else:
                raise ValidationError("El usuario al que desea enviar la transferencia no existe.")
            
    
    def validate_cant_zona_point(self,data):
        
        if data > 0:
            return data
        else:
            raise ValidationError("La transferencia debe ser mayor que 0.")
        
    
    def create(self, validated_data):
        order = TransferManagerOrderUsers.objects.create(**validated_data)
        return order
    
class BurnManagerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferManagerOrderUsers
        fields = ('id','user_manager','email','type','cant_zona_point','date','time')
        
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'user_manager':instance.user_manager.username,
            'email':instance.email,
            'type':instance.type,
            'cant_zona_point':instance.cant_zona_point,
            'date': instance.date,
            'time': instance.time,
        }
        
    def validate_email(self,data):
        user = User.objects.filter(email=data).first()
        manager = Zona0Manager.objects.filter(email=data).first()
        if manager:
            raise ValidationError("No puedes realizar una transferencia a un manager.")  
        else:
            if user and user.email == data:
                return data
            else:
                raise ValidationError("El usuario al que desea enviar la transferencia no existe.")
            
    
    def validate_cant_zona_point(self,data):
        user = User.objects.filter(email=self.initial_data['email']).first()
        if user:
            if data > 0 and user.zona_point - data > 0:
                return data
            else: raise ValidationError("No puedes quemar esa cantidad.")
        raise ValidationError("El usuario no existe.")
        
    
    def create(self, validated_data):
        order = TransferManagerOrderUsers.objects.create(**validated_data)
        order.type='Quema'
        order.save()
        return order