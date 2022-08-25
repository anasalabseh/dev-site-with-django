from pickle import FALSE
import profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Project
from .forms import ProjectForm
from .utils import searchProjects, paginateProjects

def project(request,pk):
    project_selected = Project.objects.get(id=pk)



    
    return render(request, 'project/single-project.html', {'project':project_selected})

    #the second argument in render method is the html file path and it is relative to the directory we configured in settings.py--TEMPLATES

def projects(request):
    projects, search_query= searchProjects(request)
    custom_range, projects= paginateProjects(request, projects, 6)
 
    context = {'projects': projects, 'search_query': search_query,
                'custom_range': custom_range}
    
    return render(request,'project/projects.html', context)


@login_required(login_url= 'login')
def createProject(request):
    profile= request.user.profile
    # initializing the form variable
    form = ProjectForm()
    #testing if the request method is 'post' which means the user needs to store some data in the database
    if request.method == 'POST':

        #assigning the posted information into the object
        
        #which can auto generates html form based on the model of the needed class
        #in this case we are auto creating a form and passing some values into it
        form = ProjectForm(request.POST, request.FILES)
        #recently we added the argument request.FILES it is  for processing the image file in the form
        #we added this argument in the static->images section
        #testing if everything is ok with that form and Django does that based on the functions in the model
        #"we have some arguments 'blank&"
        if form.is_valid():
            project= form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'project/project-form.html', context)


@login_required(login_url= 'login')
def updateProject(request, pk):
    profile= request.user.profile
    #we get the information of a specific object we want to update
    #only one project will be recieved
    project = profile.project_set.get(id=pk)
    #then we create an instance project form based on the project we've got
    #when we enter the form it will be automatically filled with the project's information
    form = ProjectForm(instance= project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance= project)
        if form.is_valid():
            project= form.save(commit=False)
            project.owner= profile
            project.save()
            return redirect('account')
    context= {'form': form}
    return render(request, 'project/project-form.html', context)


@login_required(login_url= 'login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    
    context = {'project': project}
    return render(request, 'project/delete-project.html', context)







