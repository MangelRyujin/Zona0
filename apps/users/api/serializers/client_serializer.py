from rest_framework import serializers
from apps.users.models import Client
from django.core.exceptions import ValidationError
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id','name','last_name','email','username','movil','password','ci')
        
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'name':instance.name,
            'last_name':instance.last_name,
            'username':instance.username,
            'email':instance.email,
            'movil':instance.movil,
            'ci':instance.ci
        }
        
    def validate_password(self,data):
        if len(data) < 8:
            raise ValidationError("La contraseña debe poseer más de 8 caracteres")
        if data.lower() == data:
            raise ValidationError("La contraseña debe poseer al menos una mayúscula")
        return data
    
    def create(self, validated_data):
        user = Client.objects.create_user(**validated_data)
        return user