from usergame import views
from django.urls import path

app_name='usergame'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'game/', views.game_api , name='game'),
    path(r'game_get_moves/', views.game_get_moves_api, name='game_get_moves'),
    ]