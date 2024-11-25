from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, UserDetailForm
from .models import Profile


class LoginUser(LoginView):
    '''
    Page for user login
    '''
    form_class = AuthenticationForm
    template_name = 'registration/login.html'


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Вход в учетную запись успешно выполнен')
                else:
                    return HttpResponse('Учетная запись отключена.')
            else:
                return HttpResponse('Ошибка учетной записи.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    '''
    Start page
    '''
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


@login_required
def edit(request):
    '''
    User data update page.
    '''
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Данные успешно обновлены.')
        else:
            messages.error(request, 'Ошибка обновления данных.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})


def register(request):
    '''
    User registration page
    '''
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def account_list(request):
    '''
    List of all users for admin
    '''
    if request.user.is_staff:
        profiles = Profile.objects.all()
    else:
        profiles = ()
    content = {
        'profiles': profiles,
    }
    return render(request, 'account/profile_list.html', content)


@login_required
def account_detail(request, pk):
    '''
    User data update page for admin.
    updated parameters: is_staff, is_active.
    '''
    print('adg', request.user, request.user.is_staff)
    if request.method == 'POST':
        profile_obj = Profile.objects.get(id=pk)
        user = profile_obj.user
        # print(user)
        form = UserDetailForm(data=request.POST)
        if form.is_valid():
            new_info = form.save(commit=False)
            if new_info.is_staff:
                user.is_staff = True
            else:
                user.is_staff = False
            if new_info.is_active:
                user.is_active = True
            else:
                user.is_active = False
            # print('adp', user, user.is_staff)
            user.save()
            return redirect(f'/account/profile_list/{pk}')
    if request.user.is_staff:
        profiles = Profile.objects.get(id=pk)
        form = UserDetailForm(instance=profiles.user)
    else:
        profiles = ()
        form = UserDetailForm()
    content = {
        'profiles': profiles,
        'form': form,
    }
    return render(request, 'account/profile_detail.html', content)
