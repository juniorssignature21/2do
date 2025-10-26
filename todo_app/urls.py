from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_task, name="add"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login_user, name="login"),
    path('edit_task/<int:pk>/', views.edit_task, name="edit_task"),
    path('delete_task/<int:pk>/', views.delete_task, name="delete_task"),
]
