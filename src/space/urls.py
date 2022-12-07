from django.urls import path

from space import views

urlpatterns = [
    path('stations/', views.SpaceStationListCreateApiView.as_view(), name="space-list"),
    path('stations/<int:pk>/', views.SpaceStationRetrieveUpdateDestroyAPIView.as_view(), name="space-detail"),
    path('stations/<int:pk>/state/', views.SpaceStationStateRetrieveCreateAPIView.as_view(), name="space-detail-state"),
]
