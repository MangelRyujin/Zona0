from rest_framework import serializers
from apps.users.models import Client
from django.core.exceptions import ValidationError
from PIL import Image
import io
from django.core.files.base import ContentFile


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id','name','last_name','email','username','movil','password','ci','image')
        
    def validate_password(self,data):
        if len(data) < 8:
            raise ValidationError("La contraseña debe poseer más de 8 caracteres")
        if data.lower() == data:
            raise ValidationError("La contraseña debe poseer al menos una mayúscula")
        return data
    
    def validate_image(self,data):
        if data:
            if data.size > 2 * 1024 * 1024:
                raise serializers.ValidationError("El archivo es demasiado grande (máximo 2MB)")
            img = Image.open(data)
            new_image_io = io.BytesIO()
            if img.format == 'JPEG':
                img.save(new_image_io, format='JPEG',optimize=True, quality=70)
            else:
                img.save(new_image_io, format=img.format)
            data.file = ContentFile(new_image_io.getvalue(), name=data.name)
        return data
    
    def create(self, validated_data):
        user = Client.objects.create_user(**validated_data)
        return user
    
    
class ClientDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id','name','last_name','username','movil','ci')
        
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'username':instance.username,
            'name':instance.name,
            'last_name':instance.last_name,
            'movil':instance.movil,
            'ci':instance.ci,
        }
    
class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id','name','last_name','username','movil','ci')
        
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'username':instance.username,
            'name':instance.name,
            'last_name':instance.last_name,
            'movil':instance.movil,
            'ci':instance.ci,
        }