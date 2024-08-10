from django.urls import path

from .views import (
    ServerViewSet,
)

urlpatterns = [
    path("/select", ServerViewSet.as_view({"get": "list"}), name="servers-list"),
    path("/<int:pk>", ServerViewSet.as_view({"get": "retrieve"}), name="servers-retrieve"),
]
