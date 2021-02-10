from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from .forms import LoginForm,UserRegistrationFrom,UserEditForm,ProfileEditForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile,Contact
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from common.decorators import ajax_required
from django.http import JsonResponse
from django.views.decorators.http  import require_POST
from actions.utils import create_action
from actions.models import Action

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
    actions=Action.objects.exclude(user=request.user)
    following_ids=request.user.following.values_list('id',flat=True)

    if following_ids:
        actions=actions.filter(user_id__in=following_ids)
    actions=actions.select_related('user','user__profile' )[:10].prefetch_related('target')

    return render(request,'account/dashboard.html',{
            'session':'dashboard',
            'actions':actions})

def register(request):
    if request.method=="POST":
        user_form=UserRegistrationFrom(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            create_action(new_user,"Created a new account")
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

@login_required
def user_list(request):
    users=User.objects.filter(is_active=True)
    return render(request,'account/user/list.html',
                {'section':'people',
                'users':users})
@login_required
def user_detail(request,username):
    user=get_object_or_404(User,username=username,is_active=True)
    return render(request,'account/user/detail.html',
                {'session':'poeple',
                'user':user})

@login_required
@ajax_required
@require_POST
def user_follow(request):
    user_id=request.POST.get('id')
    action=request.POST.get('action')
    if user_id and action:
        try:
            user=User.objects.get(id=user_id)
            if action=="follow":
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
                create_action(request.user,"is following",user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
                create_action()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})




    
