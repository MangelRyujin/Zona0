from rest_framework.routers import DefaultRouter
from apps.institution.api.views.institution_viewset import InstitutionViewSet
from apps.institution.api.views.donation_viewset import DonationViewSet



router = DefaultRouter()
router.register(r'list-institution',InstitutionViewSet, basename = 'list-institution')
router.register(r'donations',DonationViewSet, basename = 'donations')





urlpatterns = router.urls 