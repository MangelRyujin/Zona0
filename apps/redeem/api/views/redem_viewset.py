from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from apps.redeem.api.serializers.redeem_serializer import MarketingApplicanSerializer
from rest_framework.permissions import IsAuthenticated

class MarketingApplicanViewSet(viewsets.GenericViewSet):
    serializer_class= MarketingApplicanSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self,pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all().order_by('-date', '-time')
        return self.get_serializer().Meta.model.objects.filter(pk = pk).first()

    def list(self,request):
        applican = self.get_queryset()
        if applican.exists():
            applican_serializers = self.serializer_class(applican,many = True)
            return Response(applican_serializers.data, status = status.HTTP_200_OK)
        return Response({'message':'No existen aplicantes a marketing!'},status = status.HTTP_404_NOT_FOUND)
    
    
    def create(self,request):
        serializers = self.serializer_class(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status = status.HTTP_201_CREATED)
        return Response(serializers.errors,status = status.HTTP_400_BAD_REQUEST)
    
    
    
    def retrieve(self, request, pk = None):
        applican = self.get_queryset(pk)
        if applican:
            applican_serializers = self.serializer_class(applican)
            return Response(applican_serializers.data, status= status.HTTP_200_OK)
        return Response({'message':'No existe el aplicante a marketing'}, status= status.HTTP_404_NOT_FOUND)
    
    