from rest_framework import serializers
from apps.users.models import  User

   
class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('zona_point')
        
    def to_representation(self, instance):
        return {
            'orcaStore_point':instance.zona_point, 
        }
