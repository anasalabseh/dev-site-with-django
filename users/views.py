from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, SkillForm, MessageForm
from django.contrib import messages
from .forms import ProfileForm
from .utils import paginateProfiles, searchProfiles
from django.contrib.auth.models import User
from .models import Profile, Skill, Message
from django.core.paginator import Paginator
# Create your views here.

def loginUser(request):
    page= 'login'

    #in case some user manually entered the url website.com/login 
    #we can do this using decoraters

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user= User.objects.get(username= username)
            #here we check only  if the username is  in the data base
        except:
            messages.error(request, 'user does not exist')
        user = authenticate(request, username = username, password = password)       
        #what authenticate function do is returning the user instance if the password matches the username
        #or it will return NONE
        if user is not None:
            login(request, user)
            #this will create a session in the sessions table in the data base, and it will be stored in your cookies
            return redirect(request.GET['next'] if 'next' in request.GET else 'account' )
        else:
            messages.error(request, 'wrong username or password')

    return render(request, 'users/login-page.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'Succesfully Logged Out')
    return redirect('login')

def registerUser(request):
    form =CustomUserCreationForm()
    
    page= 'register'

    if request.method == 'POST':
        form =CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, 'User Account Was Created')

            login(request, user)
            return redirect('edit-account')
    
        else:
            messages.info(request, 'wrong information')
        
    context= {'page': page, 'form': form}
    return render(request, 'users/login-page.html', context)

def profiles(request):
    profiles, search_query= searchProfiles(request)
    custom_range, profiles= paginateProfiles(request, profiles, 6)

    context = {'profiles':profiles, 'search_query': search_query, 'custom_range': custom_range}

    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile =  Profile.objects.get(id=pk)
    main_skills = profile.skill_set.exclude(description= "")
    other_skills = profile.skill_set.filter(description= "")
    projects = profile.project_set.all()

    #we could make this directly in the template
    
    context= {'profile': profile, 'main_skills': main_skills, 'other_skills': other_skills, 'projects': projects}
    return render(request, 'users/single-profile.html', context)

def userAccount(request):
    profile= request.user.profile
    skills= profile.skill_set.all()
    projects= profile.project_set.all()

    context= {'profile': profile, 'skills': skills, 'projects': projects}

    return render(request, 'users/account.html', context)

@login_required(login_url= 'login')
def editAccount(request):
    profile= request.user.profile
    form= ProfileForm(instance= profile)
    #this auto fills the existing information
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance= profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context= {'form': form}
    return render(request, 'users/profile-form.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile= request.user.profile
    form= SkillForm()
    if request.method == 'POST':
        form= SkillForm(request.POST)
        if form.is_valid():
            skill= form.save(commit=False)
            skill.owner= profile
            skill.save()
            messages.success(request, 'Skill was created')
            return redirect('account')

    context= {'form': form}
    return render(request, 'users/skill-form.html', context)

@login_required(login_url= 'login')
def updateSkill(request, pk):
    profile= request.user.profile
    skill= profile.skill_set.get(id= pk)
    form= SkillForm(instance= skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance= skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill has been updated')
            return redirect('account')

    context= {'form': form}
    return render(request, 'users/skill-form.html', context)

@login_required(login_url= 'login')
def deleteSkill(request, pk):
    profile= request.user.profile
    skill = profile.skill_set.get(id= pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully')
        return redirect('account')
        
    
    context= {'skill': skill}
    return render(request, 'users/delete-skill.html', context)

@login_required(login_url= 'login')
def inbox(request):
    profile= request.user.profile
    recieved_messages= profile.messages.all()
    unread_messages_count= recieved_messages.filter(is_read= False).count()
    context= {'recieved_messages': recieved_messages, 'unread_messages_count': unread_messages_count}
    return render(request, 'users/inbox.html', context)

@login_required(login_url= 'login')
def viewMessage(request, pk):
    profile= request.user.profile
    message= profile.messages.get(id= pk)
    if message.is_read == False:
        message.is_read= True
        message.save()
    context= {'message': message}
    return render(request, 'users/message.html', context)

def sendMessage(request, pk):
    try:
        sender= request.user.profile
    except:
        sender= None

    recipient= Profile.objects.get(id=pk)
    form= MessageForm()
    if request.method == 'POST':
        form= MessageForm(request.POST)
        if form.is_valid():
            message= form.save(commit= False)
            message.sender= sender
            message.recipient= recipient
            if sender:
                message.name= sender.name
                message.email= sender.email
            message.save()
            messages.info(request, 'Your message was successfully sent')
            return redirect('user-profile', pk= recipient.id)
    context= {'form': form, 'recipient': recipient}
    return render(request, 'users/message-form.html', context)