from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from apps.orders.api.serializers.transfer_serializer import ReceiveOSPSerializer, DetailReceiveOSPSerializer
from rest_framework import status
from apps.users.models import User
from apps.users.api.serializers.point_serializer import PointSerializer
from apps.orders.models import ReceiveOSP
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# 'method' can be used to customize a single HTTP method of a view
receive_response = openapi.Response('response description', ReceiveOSPSerializer)
orcaStore_point={
  "orcaStore_point": 00.00,
}


@swagger_auto_schema(method='get', manual_parameters=None, responses={200: f'{orcaStore_point}'})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def OSP_PointView(request):
    user = get_object_or_404(User, pk=request.user.id)
    if user:
        transfer_serializer = PointSerializer(user)
        return Response(transfer_serializer.data, status = status.HTTP_200_OK)
    return Response({'message':'Usuario no existe'}, status=status.HTTP_404_NOT_FOUND)




