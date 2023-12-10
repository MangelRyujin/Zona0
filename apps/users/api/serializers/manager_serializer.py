from rest_framework import serializers
from apps.users.models import Zona0Manager
from django.core.exceptions import ValidationError
from PIL import Image
import io
from django.core.files.base import ContentFile
        
class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona0Manager
        fields = ('id','name','last_name','email','username','movil','password','ci','image')
    
        
    def validate_password(self,data):
        if len(data) < 8:
            raise ValidationError("La contraseña debe poseer más de 8 caracteres")
        if data.lower() == data:
            raise ValidationError("La contraseña debe poseer al menos una mayúscula")
        return data
    
    def validate_image(self,data):
        img = Image.open(data)
        new_image_io = io.BytesIO()
        if img.format == 'JPEG':
            img.save(new_image_io, format='JPEG',optimize=True, quality=70)
        else:
            img.save(new_image_io, format=img.format)
        data.file = ContentFile(new_image_io.getvalue(), name=data.name)
        return data
    
    def create(self, validated_data):
        user = Zona0Manager(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user