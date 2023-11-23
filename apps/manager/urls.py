from django.urls import path
from apps.manager.api.views.manager_viewset import send_ZOP,burn_ZOP

urlpatterns = [
    path("action/send-points/", send_ZOP, name="send-points"),
    path("action/burn-points/", burn_ZOP, name="burn-points"),
    
]
