from rest_framework.routers import DefaultRouter
from apps.banking.api.views.banking_viewset import BankingViewSet



router = DefaultRouter()
router.register(r'account',BankingViewSet, basename = 'account')





urlpatterns = router.urls 