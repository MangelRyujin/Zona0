from rest_framework import serializers
from apps.institution.models import Institution,Gallery


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('id','institution','image','description')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        url_sin_descarga=None
        if representation['image']:
            url = representation['image']
            url_sin_descarga = url.split("&export=download")[0]
        return {
            'id': instance.id,
            'institution' : instance.institution.institution_name,
            'image' : url_sin_descarga,
            'description' : instance.description,
            
        }
    
    
class InstitutionSerializer(serializers.ModelSerializer):
    galleryInstitution = GallerySerializer(many = True, read_only=True)
    class Meta:
        model = Institution
        fields = ('id','institution_name','institution_osp','description','image','galleryInstitution')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['image']:
            url = representation['image']
            url_sin_descarga = url.split("&export=download")[0]
            representation['image'] = url_sin_descarga
            return representation
        return representation
        

        
