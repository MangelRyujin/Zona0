from rest_framework.routers import DefaultRouter
from apps.orders.api.views.transfer_order_view import TransferOrderUsersView




router = DefaultRouter()

router.register(r'transfer-order-user', TransferOrderUsersView, basename = 'transfer-order')


urlpatterns = router.urls 