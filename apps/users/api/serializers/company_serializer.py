from django.core.exceptions import ValidationError
from rest_framework import serializers
from apps.users.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id','company_name','name','last_name','ci','type','email','company_code','movil','username','password')
        
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'company_name':instance.company_name,
            'name':instance.name,
            'last_name':instance.last_name,
            'ci':instance.ci,
            'username':instance.username,
            'movil':instance.movil,
            'email':instance.email,
            'type': instance.type,
            'company_code':instance.company_code,   
        }
    def validate_password(self,data):
        if len(data) < 8:
            raise ValidationError("La contraseña debe poseer más de 8 caracteres")
        if data.lower() == data:
            raise ValidationError("La contraseña debe poseer al menos una mayúscula")
        return data
    
    def create(self, validated_data):
        user = Company.objects.create_user(**validated_data)
        user.user_type='company'
        user.save()
        return user
    