from django.shortcuts import render,redirect,get_object_or_404
from apps.blogApp.models import BlogModel, BlogCategory, CommentModel, ReactionModel
from .forms import BlogPostForm,UpdateBlogForm,CommentForm,ReactionForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

# Create your views here.



    
def index(request):
    blogs=BlogModel.objects.all().order_by('-date_posted')
    categories=BlogCategory.objects.all()
    # filter blogs by category
    category_filter=request.GET.get('category')
    if category_filter:
        blogs=blogs.filter(category__category_name=category_filter)
    
    context={
        'blogs':blogs,
        'categories':categories,
    }
    return render(request,'Blog/index.html',context)



def detailed_page(request,blog_id):
    blog=BlogModel.objects.get(id=blog_id)
    comments=CommentModel.objects.filter(blog=blog).order_by('-date_commented')
    likes=ReactionModel.objects.filter(blog=blog,reaction=1).count()
    dislikes=ReactionModel.objects.filter(blog=blog,reaction=-1).count()
    blogs_in_same_category=BlogModel.objects.filter(category__in=blog.category.all()).exclude(id=blog_id)
    share_url = request.build_absolute_uri(blog.get_absolute_url())
    facebook_url = f'https://www.facebook.com/sharer/sharer.php?u={share_url}'
    twitter_url = f'https://twitter.com/intent/tweet?url={share_url}'
    linkedin_url = f'https://www.linkedin.com/shareArticle?url={share_url}'
    whatsapp_url = f'https://api.whatsapp.com/send?text={share_url}'

    if request.method == 'POST':
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            comment=comment_form.cleaned_data['comment']
            comment_instance=CommentModel(person=request.user.person,
                                          blog=blog,
                                          comment=comment)
            if request.user.is_authenticated:
                comment_instance.save()
                return redirect('detailed_page',blog_id=blog_id)
            else:
                messages.error(request,'You need to Login to comment')
                return redirect('login')
        
        reaction_form=ReactionForm(request.POST)
        if reaction_form.is_valid():
            reaction=reaction_form.cleaned_data['reaction']
            existing_reaction= ReactionModel.objects.filter(user=request.user,blog=blog).first()
            if existing_reaction:
                existing_reaction.reaction=reaction
                existing_reaction.save()
                return redirect('detailed_page',blog_id=blog_id)
            else:
                reaction_instance=ReactionModel(user=request.user,
                                                blog=blog,
                                                reaction=reaction)
                reaction_instance.save()
            return redirect('detailed_page',blog_id=blog_id)
    
    context={
        'blog':blog,
        'comments':comments,
        'likes':likes,
        'dislikes':dislikes,
        'blogs_in_same_category':blogs_in_same_category,
        
        'facebook_url':facebook_url,
        'twitter_url':twitter_url,
        'linkedin_url':linkedin_url,
        'whatsapp_url':whatsapp_url,
    }
    return render(request,'Blog/detailed_page.html',context)

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form=BlogPostForm(request.POST,request.FILES)
        if form.is_valid():
            title=form.cleaned_data['title']
            content=form.cleaned_data['content']
            categories=form.cleaned_data['category']
            image=form.cleaned_data['image']
            blog=BlogModel(title=title,
                           content=content,
                           image=image,
                           author=request.user.person)
            blog.save() # we need first to save the blog instance to get the id.
            # as it is a many to many relationship we need to set the relationship after saving the blog instance.
            blog.category.set(categories) # set many to many relationship
            
            return redirect('view_profile')
    else:
        form=BlogPostForm()
    return render(request,'Blog/add_blog.html',{'form':form})

@login_required
def update_blog(request,blog_id):
    blog = get_object_or_404(BlogModel, id=blog_id)
    if request.method == 'POST':
        update_form= UpdateBlogForm(request.POST, request.FILES)
        if update_form.is_valid():
            title=update_form.cleaned_data['title']
            content=update_form.cleaned_data['content']
            categories=update_form.cleaned_data['category']
            image=update_form.cleaned_data['image']

            blog.title=title
            blog.content=content
            blog.image=image
            blog.save()
            blog.category.set(categories)
            return redirect('view_profile')
    else:
        update_form=UpdateBlogForm(instance=blog)
    return render(request,'Blog/update_blog.html',{'form':update_form,'blog':blog})


def delete_blog(request,blog_id):
    blog= get_object_or_404(BlogModel, id=blog_id)
    if request.method == 'POST':
        blog.delete()
        return redirect('view_profile')
    return render(request,'Blog/delete_blog.html',{'blog':blog})


def search_blog(request):
    query = request.GET.get('q', '')  # Get the search query, or an empty string
    categories = BlogCategory.objects.all()

    if query:  # Check if the query is not empty
        multiple_query = Q(Q(title__icontains=query) | Q(content__icontains=query) | Q(category__category_name__icontains=query))
        blogs = BlogModel.objects.filter(multiple_query).distinct().order_by('-date_posted')
    else:
        blogs = BlogModel.objects.none()  # Return an empty queryset for an empty search query

    context = {
        'blogs': blogs,
        'categories': categories,
        'query': query,
    }

    if blogs:  # Check if there are search results
        return render(request, 'Blog/search_blog.html', context)
    else:
        return render(request, 'Blog/empty_search.html',context=context)