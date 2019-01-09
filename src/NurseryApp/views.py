from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import Parent, Child, Group, Teacher, Caregiver, Activity, Diet, Waiting_list
from .forms import (SignupUserForm,
                    ChildCreateForm,
                    GroupCreateForm,
                    TeacherCreateForm,
                    CaregiverCreateForm,
                    ActivityCreateForm,
                    DietCreateForm)
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
        groups = Group.objects.all()
        ctx = {
            'groups': groups,
        }
        if not user.is_superuser:
            ctx['parent'] = get_object_or_404(Parent, user=user)
        return render(request, 'main-page.html', ctx)


class ChildCreateView(CreateView):
    template_name = 'child-create-view.html'
    form_class = ChildCreateForm

    def get_initial(self):
        initial = super(ChildCreateView, self).get_initial()
        pk = self.kwargs.get('pk')
        initial['parent'] = get_object_or_404(Parent, pk=pk)
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


class CaregiverCreateView(CreateView):
    template_name = 'caregiver-create-view.html'
    form_class = CaregiverCreateForm

    def get_initial(self):
        initial = super(CaregiverCreateView, self).get_initial()
        pk = self.kwargs.get('pk')
        initial['parent'] = get_object_or_404(Parent, pk=pk)
        return initial


class CaregiverDetailView(DetailView):
    queryset = Caregiver.objects.all()
    template_name = 'caregiver-detail-view.html'


class CaregiverUpdateView(UpdateView):
    queryset = Caregiver.objects.all()
    form_class = CaregiverCreateForm
    template_name = 'caregiver-update-view.html'


class CaregiverDeleteView(DeleteView):
    model = Caregiver
    template_name = 'caregiver-delete-view.html'
    success_url = reverse_lazy('main-view')


class ActivityCreateView(CreateView):
    queryset = Activity.objects.all()
    form_class = ActivityCreateForm
    template_name = 'activity-create-view.html'


class ActivityDetailView(DetailView):
    queryset = Activity.objects.all()
    template_name = 'activity-detail-view.html'


class ActivityUpdateView(UpdateView):
    queryset = Activity.objects.all()
    form_class = ActivityCreateForm
    template_name = 'activity-update-view.html'


class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = 'activity-delete-view.html'
    success_url = reverse_lazy('main-view')


class ActivityListView(ListView):
    queryset = Activity.objects.all()
    template_name = 'activity-list-view.html'


class DietCreateView(CreateView):
    queryset = Diet.objects.all()
    form_class = DietCreateForm
    template_name = 'diet-create-view.html'


class DietDetailView(DetailView):
    queryset = Diet.objects.all()
    template_name = 'diet-detail-view.html'


class DietUpdateView(UpdateView):
    queryset = Diet.objects.all()
    form_class = DietCreateForm
    template_name = 'diet-update-view.html'


class DietDeleteView(DeleteView):
    model = Diet
    template_name = 'diet-delete-view.html'
    success_url = reverse_lazy('main-view')


class DietListView(ListView):
    queryset = Diet.objects.all()
    template_name = 'diet-list-view.html'


# class WaitingListView(View):
#     def get(self, request):
#         children = Child.objects.all()
#         return render(request, 'waiting-list-view.html', {'children': children})
