from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Person(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE,related_name='person')
    user_profile=models.ImageField(upload_to='profile_pics',default='default_profile.jpg', verbose_name= "Profile Picture" )
    user_bio=models.TextField(max_length=500, verbose_name="Bio",null=True, blank=True)
    phone_number=models.CharField(max_length=15,unique=True, verbose_name="Phone Number",null=True, blank=True)
    wanna_be_a_blogger=models.BooleanField(default=False, verbose_name="Wanna be a Blogger?",null=True, blank=True)
    user_company=models.CharField(max_length=100, verbose_name=" Your Company",null=True, blank=True)


    def __str__(self):
        return f'{self.user.username}'
    
    class Meta:
        verbose_name_plural="Person Model"