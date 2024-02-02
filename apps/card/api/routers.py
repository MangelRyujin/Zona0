from rest_framework.routers import DefaultRouter
from apps.card.api.views.card_viewset import CardViewSet
from apps.card.api.views.discountCard_viewset import DiscountCardViewSet,YourDiscountCardViewSet



router = DefaultRouter()
router.register(r'card-details',CardViewSet, basename = 'card-actions')
router.register(r'my-card-discount',DiscountCardViewSet, basename = 'my-card-discount')
router.register(r'your-card-discount',YourDiscountCardViewSet, basename = 'your-card-discount')





urlpatterns = router.urls 