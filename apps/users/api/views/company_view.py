from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.users.api.serializers.company_serializer import CompanySerializer,CompanyDetailsSerializer,CompanyUpdateSerializer
from rest_framework.permissions import IsAuthenticated



class CompanyRegisterView(viewsets.GenericViewSet):
    serializer_class= CompanySerializer
    
    def create(self, request):
        serializers = self.serializer_class(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'message':'Compañia creado correctamente!'}, status = status.HTTP_201_CREATED)
        return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)


class CompanyUpdateViewSet(viewsets.GenericViewSet):
    serializer_class= CompanyDetailsSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self,pk = None):
        if pk is not None:
            return self.serializer_class().Meta.model.objects.filter(id=pk).first()
        return None

    def list(self,request):
        pk = request.user.id
        company = self.get_queryset(pk)
        if company is not None:
            company_serializers = self.serializer_class(company)
            return Response(company_serializers.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe el usuario!'},status = status.HTTP_404_NOT_FOUND)

    def update(self,request,pk=None):
        id = request.user.id
        if pk == str(id):
            company = self.get_queryset(pk)
            if company:
                company_serializers = CompanyUpdateSerializer(company ,data = request.data)
                if company_serializers.is_valid():
                    company_serializers.save()
                    return Response(company_serializers.data, status = status.HTTP_200_OK)
                else:
                    return Response({'message':'Error al editar los datos!','errors':company_serializers.errors},status = status.HTTP_400_BAD_REQUEST) 
            return Response({'message':'No existe el usuario que desea editar!'},status = status.HTTP_404_NOT_FOUND)
        
        return Response({'message':'No puedes editar ese usuario!'},status = status.HTTP_400_BAD_REQUEST)
