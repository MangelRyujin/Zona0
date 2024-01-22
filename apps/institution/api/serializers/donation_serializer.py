from rest_framework import serializers
from apps.institution.models import Donation
from django.core.exceptions import ValidationError

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ('id','user','amount','institution')
        
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'user' : instance.user.username,
            'amount' : instance.amount,
            'institution' : instance.institution.institution_name,
        }
        
    def validate_amount(self,data):
        if data > 0:
            if self.context['user'].zona_point >= data:
                return data
            else:
                raise ValidationError("No contiene esa cantidad")
        else:
            raise ValidationError("Debe de donar un valor mayor que 0")

        
        
