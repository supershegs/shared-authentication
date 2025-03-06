from django.urls import path
from .views import ProtectedView

urlpatterns = [
    path('display', ProtectedView.as_view())
]