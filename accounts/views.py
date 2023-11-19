from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.forms import inlineformset_factory

from .forms import RegistrationForm,UserProfileForm
from .models import UserProfile

User = get_user_model()
'''
    master : admin123456
    user001 : password001
'''
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('blogBase:index'))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                request,
                username = request.POST['username'],
                password = request.POST['password1'],
            )
            login(request,new_user)  
            return redirect(reverse('blogBase:index'))
        
    else:
        form = RegistrationForm()
    return render(request,'registration/register.html',{'form':form})


@login_required
def profile(request,username):
    user = User.objects.get(username=username)
    superuser = User.objects.filter(is_superuser=True).first()
    join_users_profile = UserProfile.objects.filter(is_apply_followers=True)
    return render(request,'accounts/users_profile.html',{'user':user,'join_users_profile':join_users_profile,'superuser':superuser})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile',args=(request.user.username,)))
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request,'accounts/edit_profile.html',{'form':form})

def friends(request):
    superuser = User.objects.filter(is_superuser=True).first()
    friends = superuser.followers.all()
    unfriends = User.objects.exclude(id__in=friends).exclude(username=superuser)
    content = {
        'friends' : friends,
        'unfriends' : unfriends,
    }
    return render(request,'accounts/friends.html',content)

@login_required
def apply_join_friends(request,username):
    user = User.objects.get(username=username)
    user.profile.is_apply_followers = True
    user.profile.save()
    return render(request,'blogBase/redirect_info.html')



