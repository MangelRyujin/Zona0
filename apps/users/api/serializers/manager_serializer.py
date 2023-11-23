from rest_framework import serializers
from apps.users.models import Zona0Manager
from django.core.exceptions import ValidationError
        
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona0Manager
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
        user = Zona0Manager(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user