from rest_framework import serializers
from PIL import Image
import io
from django.core.files.base import ContentFile
from apps.users.models import User


class UpdateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','image')
        
    def validate_image(self,data):
        request = self.context.email
        if request:
            obj = User.objects.get(email=request)
            if obj.image:
                obj.image.delete(save=True)
            if data.size > 2 * 1024 * 1024:
                    raise serializers.ValidationError("El archivo es demasiado grande (máximo 2MB)")
            img = Image.open(data)
            new_image_io = io.BytesIO()
            if img.format == 'JPEG':
                img.save(new_image_io, format='JPEG',optimize=True, quality=70)
            else:
                img.save(new_image_io, format=img.format,optimize=True)
            data.file = ContentFile(new_image_io.getvalue(), name=data.name)
            return data
        else:
            raise serializers.ValidationError("Error en credenciales")
        
        