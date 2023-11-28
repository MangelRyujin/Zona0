from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.users.api.serializers.client_serializer import ClientSerializer


class ClientRegisterView(viewsets.GenericViewSet):
    serializer_class= ClientSerializer
    
    def create(self, request):
        serializers = self.serializer_class(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'data':serializers.data}, status = status.HTTP_201_CREATED)
            # return Response({'message':'Cliente creado correctamente!'}, status = status.HTTP_201_CREATED)
        return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)