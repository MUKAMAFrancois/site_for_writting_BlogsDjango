from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='home'),
    path('blog/<int:blog_id>/', views.detailed_page, name='detailed_page'),
    path('create_blog/', views.create_blog_post, name='create_blog'),
    path('update_blog/<int:blog_id>/', views.update_blog, name='update_blog'),
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('search_blog/', views.search_blog, name='search_blog')
    

]