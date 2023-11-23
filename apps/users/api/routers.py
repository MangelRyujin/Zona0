from rest_framework.routers import DefaultRouter
from apps.users.api.views.client_view import ClientRegisterView
from apps.users.api.views.company_view import CompanyRegisterView



router = DefaultRouter()

router.register(r'client', ClientRegisterView, basename = 'client')
router.register(r'company', CompanyRegisterView, basename = 'company')


urlpatterns = router.urls 