from django.db import models
from apps.accounts.models import Person
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.




category_choices=(
    ('Technology','Technology'),
    ('Health','Health'),
    ('Fashion','Fashion'),
    ('Food','Food'),
    ('Travel','Travel'),
    ('Sports','Sports'),
    ('Music','Music'),
    ('Movies','Movies'),
    ('Books','Books'),
    ('Fitness','Fitness'),
    ('Business','Business'),
    ('Politics','Politics'),
    ('Science','Science'),
    ('Art','Art'),
    ('Education','Education'),
    ('Lifestyle','Lifestyle'),
    ('Other','Other'),

)

class BlogCategory(models.Model):
    category_name=models.CharField(max_length=100, verbose_name="Category Name", choices=category_choices,default='Technology')


    def __str__(self):
        return self.category_name
    

class CommentModel(models.Model):
    person=models.ForeignKey(Person, on_delete=models.CASCADE, related_name='comment_person',default=None)
    blog=models.ForeignKey('BlogModel', on_delete=models.CASCADE, related_name='comments_blog')
    comment=models.TextField(verbose_name="Comment")
    date_commented=models.DateTimeField(auto_now_add=True, verbose_name="Date Commented")

    def __str__(self):
        return f'{self.person.user.username} Commented on {self.blog.title}'

  


class ReactionModel(models.Model):
    REACTION_CHOICES = (
        (-1, 'Dislike'),
        (0, 'No Reaction'),
        (1, 'Like'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    blog = models.ForeignKey('BlogModel', on_delete=models.CASCADE, related_name='reactions')
    reaction = models.IntegerField(choices=REACTION_CHOICES, default=0)
    date_reacted = models.DateTimeField(auto_now=True, verbose_name="Date Reacted")


    def __str__(self):
        return f'{self.user.username} Reacted on {self.blog.title}'
    
    class Meta:
        unique_together = ('user', 'blog') # A person can react to a blog only once
        verbose_name = "Reaction Model"



class BlogModel(models.Model):
    title=models.CharField(max_length=100, verbose_name="Title")
    author=models.ForeignKey(Person, on_delete=models.CASCADE,related_name='author_blogs')
    category=models.ManyToManyField(BlogCategory, related_name='blog_categories')
    content=RichTextField(verbose_name="Content")
    image=models.ImageField(upload_to='blog_pics',default='default_blog.jpg', verbose_name= "Blog Image" )
    date_posted=models.DateField(auto_now_add=True, verbose_name="Date Posted",null=True, blank=True)
    last_updated=models.DateField(auto_now=True, verbose_name="Last Updated",null=True, blank=True)
    views=models.PositiveBigIntegerField(default=0, verbose_name="Views")
   

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detailed_page', kwargs={'blog_id': self.id})

    class Meta:
        verbose_name_plural="Blog Models"

