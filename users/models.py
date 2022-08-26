import email
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    #OneToOneField is simply the class Profile extends the class User
    name = models.CharField(max_length= 100, null= True, blank= True)
    username = models.CharField(max_length= 100, null= True, blank= True)
    email = models.EmailField(max_length= 500, null=True, blank=True)
    location =  models.CharField(max_length= 100, null= True, blank= True)
    short_intro = models.CharField(max_length= 200, null= True, blank= True)
    bio = models.TextField(max_length= 500, null= True, blank= True)
    profile_image = models.ImageField(null= True, blank= True, upload_to= 'profiles/', default = 'profiles/user-default.png')
    social_twitter= models.CharField(max_length= 100, null= True, blank= True)
    social_linkedin= models.CharField(max_length= 100, null= True, blank= True)
    social_github = models.CharField(max_length= 100, null= True, blank= True)
    social_website = models.CharField(max_length= 100, null= True, blank= True)
    social_youtube= models.CharField(max_length= 100, null= True, blank= True)
    created = models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):

        return str(self.user.username)

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE, null= True, blank= True)
    name = models.CharField(max_length= 200, null= True, blank= True)
    description = models.TextField(max_length= 500, null= True, blank= True)

    created = models.DateTimeField(auto_now_add=True)
   
    id= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

class Messege(models.Model):
    sender= models.ForeignKey(Profile, on_delete= models.SET_NULL, null= True)
    recipient= models.ForeignKey(Profile, on_delete= models.SET_NULL, null= True, related_name= "messages")
    #what related_name attribute does, we can call the related messages of a particuler profile using profile.messages
    #instead of Profile.message_set.all
    name= models.CharField(max_length= 150, blank= True, null= True, )
    email= models.CharField(max_length= 250, blank= True, null= True)
    subject= models.CharField(max_length= 200, blank= True, null= True)
    body= models.TextField()
    is_read= models.BooleanField(default= False, null=True)

    created = models.DateTimeField(auto_now_add=True)
   
    id= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject
    
    class Meta:
        ordering= ['is_read', '-created', 'subject']

