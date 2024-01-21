from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.institution.api.serializers.institution_serializer import InstitutionSerializer
from rest_framework.permissions import IsAuthenticated


class InstitutionViewSet(viewsets.GenericViewSet):
    serializer_class= InstitutionSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self,pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(active = True)
        return self.get_serializer().Meta.model.objects.filter(id = pk).filter(active = True).first()

    def list(self,request):
        institution = self.get_queryset()
        if institution.exists():
            institution_serializers = self.serializer_class(institution,many = True)
            return Response(institution_serializers.data, status = status.HTTP_200_OK)
        return Response({'error':'No existen instituciones!'},status = status.HTTP_404_NOT_FOUND)
    
    def retrieve(self, request, pk = None):
        institution = self.get_queryset(pk)
        if institution:
            institution_serializers = self.serializer_class(institution)
            return Response(institution_serializers.data, status= status.HTTP_200_OK)
        return Response({'message':'No existe la institucion'}, status= status.HTTP_404_NOT_FOUND)