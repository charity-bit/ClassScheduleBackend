from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


# Create your models here.
class User(AbstractUser):
    # User Types
    TECHNICAL_MENTOR = 'TM'
    STUDENT = 'STUD'
    
    USER_TYPES = (
        (STUDENT,'Student'),
        (TECHNICAL_MENTOR,'Technical Mentor')
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)
    user_type = models.CharField(max_length=4,choices=USER_TYPES,default=STUDENT)
    
    username = None


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return f'{self.email}'


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_image = CloudinaryField('image')
    bio = models.TextField()

    











