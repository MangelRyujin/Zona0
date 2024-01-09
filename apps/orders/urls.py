from django.urls import path
from apps.orders.api.views.receive_view import CreateReceiveOSPView,ListUnpaidReceiveOSPView,DeleteUnpaidReceiveOSPView,ListPaidReceiveOSPView

urlpatterns = [
    path("create-receive/", CreateReceiveOSPView, name="create-receive"),
    path("list-unpaid-receive/", ListUnpaidReceiveOSPView, name="list-unpaid-receive"),
    path("list-paid-receive/", ListPaidReceiveOSPView, name="list-paid-receive"),
    path("list-delete-unpaid-receive/<int:id>", DeleteUnpaidReceiveOSPView, name="list-delete-unpaid-receive"),
    
]