from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_page, name='profile_page'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/update/', views.project_update, name='project_update'),
    path('projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('projects/<int:project_id>/clone/', views.project_clone, name='project_clone'),
    path('projects/<int:project_id>/', views.design_page, name='design_page'),
    path('projects/<int:project_id>/chat/', views.chat_message, name='chat_message'),
]
