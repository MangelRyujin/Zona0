from rest_framework.routers import DefaultRouter
from apps.redeem.api.views.redeemCode_viewset import CodeViewSet





router = DefaultRouter()
router.register(r'code',CodeViewSet, basename = 'code')


urlpatterns = router.urls 