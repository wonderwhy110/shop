from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
#forom .views import Register

app_name = 'shop'
urlpatterns = [
path('', views.product_list, name='product_list'),  # Все продукты
path('login/', auth_views.LoginView.as_view(), name='login'),
path('register/', views.register, name='register'),
path('register_done/', views.register_done, name='register_done'),

path('video/', views.video, name='video'),

 path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
 path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
 #path('register/', Register.as_view(), name='register'),

 path('logout/', auth_views.LogoutView.as_view(), name='logout'),



]