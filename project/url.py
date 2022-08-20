from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name="projects"),

    path('project/<str:pk>/', views.project, name="project"),

    path('create-project/', views.createProject, name="create-project"),

    path('update-project/<str:pk>', views.updateProject, name="update-project"),

    #when i forgot the <str:pk> argument and gave an id it gave an  error "Exeption.Reverse"
    #reverse 'update-project' has no argument (uuid(etc),)

    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project"),




]