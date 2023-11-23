from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.orders.api.serializers.order_serializer import TransferOrderUsersSerializer
from utils.send_email.send_email import send_email_transfer
from apps.users.models import User


class TransferOrderUsersView(viewsets.GenericViewSet):
    serializer_class= TransferOrderUsersSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self,user_id=None,pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(user=user_id).order_by('-date','-time')[:10]
        return self.get_serializer().Meta.model.objects.filter(id = pk).first() 
    
    def list(self, request, *args, **kargs):
        orders = self.get_queryset(request.user,pk=None)
        if orders.exists():
            orders_serializers = self.serializer_class(orders,many = True)
            return Response(orders_serializers.data, status= status.HTTP_200_OK)
        return Response({'message':'No existen transferencias'}, status= status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        serializers = self.serializer_class(data = request.data)
        if serializers.is_valid():
            send_email_transfer(request.user,request.data['email'],request.data['cant_zona_point'])
            serializers.save()
            data = serializers.data
            user = User.objects.filter(id = request.data['user']).first()
            user2 = User.objects.filter(email = request.data['email']).first()
            user.burn_zop(data['cant_zona_point'])
            user2.transfer_zop(data['cant_zona_point'])
            return Response({'message':'Transferencia efectuada correctamente!'}, status = status.HTTP_201_CREATED)
        return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)
