from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User

from .models import Parent
from .forms import SignupUserForm
from django.views.generic import View


class NurseryLoginView(LoginView):
    template_name = 'login-page.html'


class NurseryLogoutView(LogoutView):
    next_page = reverse_lazy('login-view')


class SignupView(View):
    def get(self, request):
        form = SignupUserForm()
        return render(request, 'signup-page.html', {'form': form})

    def post(self, request):
        form = SignupUserForm(request.POST)
        ctx = {'form': form}
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            parent = Parent.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
            parent.save()
            user.save()
            return redirect('main-view')
        return render(request, 'signup-page.html', ctx)


class MainPageView(View):
    def get(self, request):
        return render(request, 'main-page.html', {})
