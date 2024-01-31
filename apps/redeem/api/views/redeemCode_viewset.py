from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.redeem.api.serializers.redeem_serializer import CodeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from apps.redeem.models import Code
from apps.users.models import User

class CodeViewSet(viewsets.GenericViewSet):
    serializer_class= CodeSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self,code = None):
        if code is None:
            return None
        return self.get_serializer().Meta.model.objects.filter(code = code).first()

    
    @action(detail = False, methods = ['post'])
    def redeem(self,request):
        if request.data['code']:
            code = self.get_queryset(request.data['code'].strip())
            if code:
                if code.redeem:
                    return Response({'error':'Código ya canjeado'}, status= status.HTTP_400_BAD_REQUEST)
                else: 
                    user = get_object_or_404(User, pk=request.user.id)
                    if user:
                        if code.prize_fund > 0: 
                            code.redeem_code()
                            user.transfer_zop(code.prize_fund)
                            amount=code.prize_fund
                            code.burn_code()
                            return Response({'message':f'Felicitaciones usted ha recivido {amount} OSP!!!!'}, status= status.HTTP_200_OK)
                        code.redeem_code()
                        return Response({'message':'Lo sentimos no ha ganado ningun premio'}, status= status.HTTP_200_OK)
                    return Response({'error':'No existe su usuario'}, status= status.HTTP_404_NOT_FOUND)
            return Response({'error':'No existe el código'}, status= status.HTTP_404_NOT_FOUND)
        return Response({'error':'Introduzca un codigo por favor'}, status= status.HTTP_400_BAD_REQUEST)
                
            
        