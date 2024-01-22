from rest_framework.routers import DefaultRouter
from apps.redeem.api.views.redem_viewset import MarketingApplicanViewSet




router = DefaultRouter()
router.register(r'applican',MarketingApplicanViewSet, basename = 'applican')





urlpatterns = router.urls 