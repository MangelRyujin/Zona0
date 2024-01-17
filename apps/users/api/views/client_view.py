from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.users.api.serializers.client_serializer import ClientSerializer, ClientUpdateSerializer,ClientDetailsSerializer
from rest_framework.permissions import IsAuthenticated

class ClientRegisterView(viewsets.GenericViewSet):
    serializer_class= ClientSerializer
    
    def create(self, request):
        serializers = self.serializer_class(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'message':'Cliente creado correctamente!'}, status = status.HTTP_201_CREATED)
        return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)
    
class ClientUpdateViewSet(viewsets.GenericViewSet):
    serializer_class= ClientDetailsSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self,pk = None):
        if pk is not None:
            return self.serializer_class().Meta.model.objects.filter(id=pk).first()
        return None

    def list(self,request):
        pk = request.user.id
        client = self.get_queryset(pk)
        if client is not None:
            client_serializers = self.serializer_class(client)
            return Response(client_serializers.data, status = status.HTTP_200_OK)
        return Response({'error':'No existe el usuario!'},status = status.HTTP_404_NOT_FOUND)

    def update(self,request,pk=None):
        id = request.user.id
        if pk == str(id):
            client = self.get_queryset(pk)
            if client:
                client_serializers = ClientUpdateSerializer(client ,data = request.data)
                if client_serializers.is_valid():
                    client_serializers.save()
                    return Response(client_serializers.data, status = status.HTTP_200_OK)
                else:
                    return Response({'message':'Error al editar los datos!','errors':client_serializers.errors},status = status.HTTP_400_BAD_REQUEST) 
            return Response({'message':'No existe el usuario que desea editar!'},status = status.HTTP_404_NOT_FOUND)
        
        return Response({'message':'No puedes editar ese usuario!'},status = status.HTTP_400_BAD_REQUEST)
