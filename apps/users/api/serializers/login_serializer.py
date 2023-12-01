from dj_rest_auth.serializers import LoginSerializer,UserDetailsSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model



# class CompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = ['company_name', 'company_code', 'type', 'correct_company']

class EmailVerificationLoginSerializer(LoginSerializer):
    """
    Custom login serializer that verifies the status of the email confirmation
    """

    def validate(self, attrs):
        """
        Validates that the user has confirmed the email address

        Raises:
            ValidationError: if the email address is not confirmed
        """

        attrs = super().validate(attrs)
        user = attrs["user"]
        if user.is_superuser or user.verified_email:
            return attrs
        raise serializers.ValidationError(_("E-mail no verificado."))


class CustomUserDetailsSerializer(UserDetailsSerializer):
    
    class Meta(UserDetailsSerializer.Meta):
       model = get_user_model()
       
       fields = UserDetailsSerializer.Meta.fields + ('name','image')
       
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['image']:
            url = representation['image']
            url_sin_descarga = url.split("&export=download")[0]
            representation['image'] = url_sin_descarga
            return representation
        return representation
        
        
        
        