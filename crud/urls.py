from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('dashboard/', views.dashboard, name='dashboard'),

    path('gender/list', views.gender_list, name='gender_list'),
    path('gender/add', views.add_gender, name='gender_add'),
    path('gender/delete/<int:id>/', views.delete_gender, name='gender_delete'),
    path('gender/update/<int:id>/', views.update_gender, name='gender_update'),


    path('user/list', views.user_list, name='user_list'),
    path('user/add', views.add_user, name='user_add'),
    path('user/delete/<int:id>/', views.delete_user, name='user_delete'),
    path('user/update/<int:id>/', views.update_user, name='user_update'),
]