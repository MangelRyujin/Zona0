from rest_framework.routers import DefaultRouter
from apps.institution.api.views.institution_viewset import InstitutionViewSet



router = DefaultRouter()
router.register(r'list-institution',InstitutionViewSet, basename = 'list-institution')





urlpatterns = router.urls 