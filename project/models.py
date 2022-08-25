from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile, blank= True, null= True, on_delete= models.SET_NULL)
    #max_length is a required attribute for function CharField
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    #the path in default is appended to MEDIA_ROOT path
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags= models.ManyToManyField('Tag', blank=True)
    vote_count= models.IntegerField(default=0, null=True, blank=True)
    vote_ratio= models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    #auto_now_add will auto generate time the project has been created
    id= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    #the first attribute is for the encryption type
   
    def __str__(self):
        #this function will change the string viewed on the admin table
        #instead of viewing the id and many other things we only view th project title
        return self.title
    
    class Meta:
        ordering= ['-vote_ratio', '-vote_count', 'title']
    
    
    @property
    def getVoteCount(self):
        reviews= self.review_set.all()
        total_reviews= reviews.count()
        positive_votes= reviews.filter(value= 'up').count()
        ratio= int(positive_votes/total_reviews) * 100
        self.vote_count= total_reviews
        self.vote_ratio= ratio
        self.save()


class Review(models.Model):
    VOTE_TYPE= (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner= models.ForeignKey(Profile, on_delete= models.CASCADE, null= True)
    project=models.ForeignKey(Project, on_delete= models.CASCADE)
    #this simply means that when we delete this project all the reviews that connected to this project will be deleted as well
    #although, if we set the on_delete property to SET_NULL then the reviews will be left alone but the project property will be null
    body= models.TextField(null=True, blank=True)
    value= models.CharField(max_length=200, choices= VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together= [['owner', 'project']]

    def __str__(self):
        return self.value
    


class Tag(models.Model):
    name= models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id= models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

#in the one to many relationship we only specify a foreign key in the child who has the many relation side
#in many to many we've set the relation in the primary model """not sure"""