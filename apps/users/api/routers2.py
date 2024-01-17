from rest_framework.routers import DefaultRouter
from apps.users.api.views.client_view import ClientUpdateViewSet
from apps.users.api.views.company_view import CompanyUpdateViewSet


router = DefaultRouter()

router.register(r'client-update', ClientUpdateViewSet, basename = 'client-update')
router.register(r'company-update', CompanyUpdateViewSet, basename = 'company-update')




urlpatterns = router.urls 