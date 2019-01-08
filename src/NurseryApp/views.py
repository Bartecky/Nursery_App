from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import Parent, Child, Group, Teacher
from .forms import SignupUserForm, ChildCreateForm, GroupCreateForm, TeacherCreateForm
from django.views.generic import View, CreateView, DetailView, UpdateView, DeleteView, ListView


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
            data = form.cleaned_data
            user = User(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'])
            user.set_password(data['password'])
            user.save()
            parent = Parent.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
            parent.save()
            user_auth = authenticate(username=data['username'], password=data['password'])
            login(request, user_auth)
            return redirect('main-view')
        return render(request, 'signup-page.html', ctx)


class MainPageView(View):
    def get(self, request):
        user = get_object_or_404(User, id=self.request.user.id)
        parent = get_object_or_404(Parent, user=user)
        return render(request, 'main-page.html', {'parent': parent})


class ChildCreateView(CreateView):
    template_name = 'child-create-view.html'
    form_class = ChildCreateForm
    success_url = reverse_lazy('main-view')

    def get_initial(self):
        initial = super(ChildCreateView, self).get_initial()
        id_ = self.kwargs.get('pk')
        initial['parent'] = get_object_or_404(Parent, id=id_)
        return initial


class ChildDetailView(DetailView):
    queryset = Child.objects.all()
    template_name = 'child-detail-view.html'


class ChildUpdateView(UpdateView):
    queryset = Child.objects.all()
    form_class = ChildCreateForm
    template_name = 'child-update-view.html'


class ChildDeleteView(DeleteView):
    model = Child
    template_name = 'child-delete-view.html'
    success_url = reverse_lazy('main-view')


class GroupListView(ListView):
    queryset = Group.objects.all()
    template_name = 'group-list-view.html'


class GroupCreateView(CreateView):
    template_name = 'group-create-view.html'
    form_class = GroupCreateForm
    success_url = reverse_lazy('group-list-view')


class GroupDetailView(DetailView):
    queryset = Group.objects.all()
    template_name = 'group-detail-view.html'


class GroupUpdateView(UpdateView):
    queryset = Group.objects.all()
    form_class = GroupCreateForm
    template_name = 'group-update-view.html'
    success_url = reverse_lazy('group-list-view')



class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'group-delete-view.html'
    success_url = reverse_lazy('group-list-view')


class TeacherCreateView(CreateView):
    template_name = 'teacher-create-view.html'
    form_class = TeacherCreateForm
    success_url = reverse_lazy('teacher-list-view')


class TeacherDetailView(DetailView):
    queryset = Teacher.objects.all()
    template_name = 'teacher-detail-view.html'

class TeacherUpdateView(UpdateView):
    queryset = Teacher.objects.all()
    form_class = TeacherCreateForm
    template_name = 'teacher-update-view.html'
    success_url = reverse_lazy('teacher-list-view')


class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'teacher-delete-view.html'
    success_url = reverse_lazy('teacher-list-view')


class TeacherListView(ListView):
    queryset = Teacher.objects.all()
    template_name = 'teacher-list-view.html'
