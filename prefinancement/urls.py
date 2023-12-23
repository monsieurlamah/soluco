from django.urls import path
from prefinancement import views

urlpatterns = [
    path('compte/', views.account, name="prefinancement-compte"),
    path('terrain/', views.clientTerrain_register, name="prefinancement-terrain"),
    path('construction/', views.clientContruction_register, name="prefinancement-construction"),
]
