from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.users.api.serializers.image_serializer import UpdateImageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

    
class ImageView(APIView):
   serializer_class = UpdateImageSerializer
   permission_classes = [IsAuthenticated]
   
   def put(self, request):
       # Aquí va la lógica de tu vista
       
        serializers = self.serializer_class(request.user,data = request.data,context=request.user)
        if serializers.is_valid():
            serializers.save()
            return Response({'message':'Imagen editada!'}, status = status.HTTP_200_OK)
        return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)