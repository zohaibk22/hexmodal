from django.urls import path
from .views import IngestPayloadView, DeviceView


urlpatterns = [
    path('/payload', IngestPayloadView.as_view(), name='payloads'),
    path('/devices', DeviceView.as_view(), name='Devices')
]