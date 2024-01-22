from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.institution.api.serializers.donation_serializer import DonationSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.users.models import User
from apps.institution.models import Institution

class DonationViewSet(viewsets.GenericViewSet):
    serializer_class= DonationSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self,pk = None,user=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(user = user)[:30]
        return self.get_serializer().Meta.model.objects.filter(user = user).filter(pk = pk).first()

    def list(self,request):
        donations = self.get_queryset(None,request.user.id)
        if donations.exists():
            donations_serializers = self.serializer_class(donations,many = True)
            return Response(donations_serializers.data, status = status.HTTP_200_OK)
        return Response({'message':'No existen donaciones!'},status = status.HTTP_404_NOT_FOUND)
    
    def create(self,request):
        data = {'user':request.user.id,'amount':request.data['amount'],'institution':request.data['institution']}
        serializers = self.serializer_class(data = data, context={'user':request.user})
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status = status.HTTP_201_CREATED)
        return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)
    
    
    def retrieve(self, request, pk = None):
        donations = self.get_queryset(pk,request.user.id)
        if donations:
            donations_serializers = self.serializer_class(donations)
            return Response(donations_serializers.data, status= status.HTTP_200_OK)
        return Response({'message':'No existe la donacion'}, status= status.HTTP_404_NOT_FOUND)
    
    