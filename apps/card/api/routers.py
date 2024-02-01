from rest_framework.routers import DefaultRouter
from apps.card.api.views.card_viewset import CardViewSet



router = DefaultRouter()
router.register(r'card-actions',CardViewSet, basename = 'card-actions')





urlpatterns = router.urls 