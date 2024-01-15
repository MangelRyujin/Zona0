from django.urls import path
from apps.orders.api.views.receive_view import CreateReceiveOSPView,ListUnpaidReceiveOSPView,DeleteUnpaidReceiveOSPView,ListPaidReceiveOSPView,DetailReceiveOSPView
from apps.orders.api.views.sendTransfer_view import CreateTransferOSPView,ListSendTrasferOSPView
urlpatterns = [
    path("create-receive/", CreateReceiveOSPView, name="create-receive"),
    path("list-unpaid-receive/", ListUnpaidReceiveOSPView, name="list-unpaid-receive"),
    path("list-paid-receive/", ListPaidReceiveOSPView, name="list-paid-receive"),
    path("detail-receive/", DetailReceiveOSPView, name="detail-receive"),
    path("list-delete-unpaid-receive/<int:id>", DeleteUnpaidReceiveOSPView, name="list-delete-unpaid-receive"),
    path("create-sendTransfer/", CreateTransferOSPView, name="create-sendTRansfer"),
    path("list-sendTransfer/", ListSendTrasferOSPView, name="list-sendTRansfer"),
]