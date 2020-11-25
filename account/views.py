from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from .forms import LoginForm,UserRegistrationFrom,UserEditForm,ProfileEditForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.

def user_login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Invalid account')
    else:
        form=LoginForm()

    return render(request,'account/login.html',{
            'form':form
        })

@login_required
def dashboard(request):
    return render(request,'account/dashboard.html',
            {'section':'dashboard'})

def register(request):
    if request.method=="POST":
        user_form=UserRegistrationFrom(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            #create empty profile for the new user
            Profile.objects.create(user=new_user)


            
            return render(request,'account/register_done.html',
                                   {'new_user':new_user})
    else:
        user_form=UserRegistrationFrom()
    return render(request,'account/register.html',
                            {'user_form':user_form})

@login_required
def edit(request):
    if request.method=='POST':
        user_form=UserEditForm(request.POST,instance=request.user)
        profile_form=ProfileEditForm(request.POST,instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html',
                    {
                        'user_form':user_form,
                        'profile_form':profile_form
                    }
                 )


    
