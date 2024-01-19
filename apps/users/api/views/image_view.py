from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.users.api.serializers.image_serializer import UpdateImageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.users.models import User

    
class ImageView(APIView):
   serializer_class = UpdateImageSerializer
   permission_classes = [IsAuthenticated]
   
   def put(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        serializers = self.serializer_class(user,data = request.data,context=request.user)
        if serializers.is_valid():
            serializers.save()
            user = get_object_or_404(User, pk=request.user.id)
            return Response({'image':user.image.url.split("&export=download")[0]}, status = status.HTTP_200_OK)
        return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)
    
    