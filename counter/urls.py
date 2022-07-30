from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('get-ships-data/', views.get_ships_data, name='get-ships-data'),
        path('shipsPage/', views.ships_page , name='shipsPage'),
        path('locationPage/', views.location_page , name='locationPage'),
        path('shipsLocations/', views.ships_locations , name='shipsLocations'),
]
