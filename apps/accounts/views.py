from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import ProfileCreationForm,RegistrationForm,LoginForm,ProfileUpdateForm
from django.contrib import messages
from apps.accounts.models import Person
from django.contrib.auth.decorators import login_required
from apps.blogApp.models import BlogModel,ReactionModel

# Create your views here.




def signup_view(request):
    
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            confirm_password=form.cleaned_data['confirm_password']
            if password==confirm_password:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Email already exists')
                    return redirect('signup')
                else:
                    user=User.objects.create_user(first_name=first_name,
                                                  last_name=last_name,
                                                  email=email,
                                                  password=password, 
                                                  username=email)
                    user.save()
                    return redirect('login')
            else:
                messages.error(request,'Passwords do not match')
                return redirect('signup')
    else:
        form=RegistrationForm()
    return render(request,'Users/register.html',{'form':form})

@login_required
def create_profile(request):
    if request.method == 'POST':
        form=ProfileCreationForm(request.POST,request.FILES)
        if form.is_valid():
            user_bio=form.cleaned_data['user_bio']
            phone_number=form.cleaned_data['phone_number']
            wanna_be_a_blogger=form.cleaned_data['wanna_be_a_blogger']
            user_company=form.cleaned_data['user_company']
            user_profile=form.cleaned_data['user_profile']
            user=request.user
#  we need to first check if the User already has a related Person instance. 
#If it does, we should update the existing Person instance instead of creating a new one.
# Because we are using OneToOneField.
            
            try:
                person = user.person
                """
                In Django, when you define a OneToOneField or a ForeignKey on a model,
                  Django automatically creates a reverse relation on the related model.
                    In your case, since you have a OneToOneField from Person to User, 
                Django creates a person attribute on the User model,
                  which allows you to access the related Person instance from the User instance.
                """
                person.user_bio=user_bio
                person.phone_number=phone_number
                person.wanna_be_a_blogger=wanna_be_a_blogger
                person.user_company=user_company
                person.user_profile=user_profile

                person.save()
            except Person.DoesNotExist:
                person =Person.objects.create(user=user,
                                                user_bio=user_bio,
                                                phone_number=phone_number,
                                                wanna_be_a_blogger=wanna_be_a_blogger,
                                                user_company=user_company,
                                                user_profile=user_profile)
                person.save()
            messages.success(request,'Profile created successfully')
            if user.is_authenticated:
                    return redirect('home')
            return redirect('login')
    else:
        form=ProfileCreationForm()
    return render(request,'Users/create_profile.html',{'form':form})




def login_view(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=authenticate(request, username=User.objects.get(email=email),password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Invalid credentials')
                return redirect('login')
    else:
        form=LoginForm()
    return render(request,'Users/login.html',{'form':form})


def logout_view(request):
    logout(request)
    messages.success(request,'Logout successful')
    return redirect('login')


@login_required
def view_profile(request):
    user=request.user
    person=user.person
    my_blogs = BlogModel.objects.filter(author=person)
    for blog in my_blogs:
        likes = ReactionModel.objects.filter(blog=blog,reaction=1).count()
    context={
        'person':person,
        'my_blogs':my_blogs,
        'likes':likes,
      
    }
    return render(request,'Users/view_profile.html',context=context)


@login_required
def update_profile(request):
    user=request.user
    try:
        person=user.person
    except Person.DoesNotExist:
        person=None
    if request.method == 'POST':
        form=ProfileUpdateForm(request.POST,request.FILES,instance=person)
        if form.is_valid():
            user_bio=form.cleaned_data['user_bio']
            phone_number=form.cleaned_data['phone_number']
            wanna_be_a_blogger=form.cleaned_data['wanna_be_a_blogger']
            user_company=form.cleaned_data['user_company']
            user_profile=form.cleaned_data['user_profile']
            try:
                person = user.person
                person.user_bio=user_bio
                person.phone_number=phone_number
                person.wanna_be_a_blogger=wanna_be_a_blogger
                person.user_company=user_company
                person.user_profile=user_profile

                person.save()
            except Person.DoesNotExist:
                person =Person.objects.create(user=user,
                                                user_bio=user_bio,
                                                phone_number=phone_number,
                                                wanna_be_a_blogger=wanna_be_a_blogger,
                                                user_company=user_company,
                                                user_profile=user_profile)
                person.save()
            messages.success(request,'Profile updated successfully')
            return redirect('view_profile')
    else:
        form=ProfileUpdateForm(instance=person)

    context={
        'form':form,
        'person':person
    }
    return render(request,'Users/update_profile.html',context)