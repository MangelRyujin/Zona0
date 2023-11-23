from rest_framework.response import Response
from rest_framework import status
from apps.users.api.serializers.manager_serializer import ManagerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.users.models import User
from utils.send_email.send_email import send_email_create_manager_incorrect

class ManagerCreateView(APIView):
   serializer_class = ManagerSerializer
   permission_classes = [IsAuthenticated]
   
   def post(self, request, format=None):
       # Aquí va la lógica de tu vista
        if request.user.is_superuser == True:
                serializers = self.serializer_class(data = request.data)
                if serializers.is_valid():
                        serializers.save()
                        return Response({'message':'Manager creado correctamente!'}, status = status.HTTP_201_CREATED)
                return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
                user = User.objects.filter(id = request.user.id).first()
                user.is_active = False
                user.is_staff = False
                user.save()
                send_email_create_manager_incorrect(request.user,request.user.email)
                return Response({"message": "Este usuario no tiene permiso para crear manager has sido vaneado hasta nuevo aviso"})

        