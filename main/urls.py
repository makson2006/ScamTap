from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from main import views
urlpatterns = [
    path('add_points/', views.add_points, name='add_points'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='user_login'),
    path('buy_miner/', views.buy_miner, name='buy_miner'),
    path('gamble/', views.gamble_view, name='gamble'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
