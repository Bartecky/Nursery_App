from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as UserGroup
from django.contrib.auth import login, authenticate
from .models import Parent, Child, Group, Teacher, Caregiver, Activity, Diet
from .forms import (SignupUserForm,
                    ChildCreateForm,
                    GroupCreateForm,
                    TeacherCreateForm,
                    CaregiverCreateForm,
                    ActivityCreateForm,
                    DietCreateForm,
                    AddingChildToGroupForm,
                    AddingTeacherToGroupForm,
                    )
from django.views.generic import View, CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib import messages
import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class NurseryLoginView(LoginView):
    template_name = 'login-page.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main-view')
        return super(NurseryLoginView, self).get(request)


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
                last_name=data['last_name']
            )
            user.set_password(data['password'])
            user.save()
            parent = Parent.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
            parent.save()
            grp = get_object_or_404(UserGroup, name='parents')
            user.groups.add(grp)
            user_auth = authenticate(username=data['username'], password=data['password'])
            login(request, user_auth)
            return redirect('main-view')
        return render(request, 'signup-page.html', ctx)


class MainPageView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(User, id=self.request.user.id)
        groups = Group.objects.all().order_by('pk')
        diets = Diet.objects.all().order_by('name')
        activities = Activity.objects.all().order_by('name')
        teachers = Teacher.objects.all()
        # messages = Message.objects.all()
        ctx = {
            'groups': groups,
            'diets': diets,
            'activities': activities,
            'teachers': teachers
            # 'messages': messages
        }
        if not user.is_superuser:
            ctx['parent'] = get_object_or_404(Parent, user=user)
        return render(request, 'main-page.html', ctx)


class ChildCreateView(CreateView):
    template_name = 'child-create-view.html'
    form_class = ChildCreateForm
    permission_required = 'NurseryApp.add_child'

    def get_initial(self):
        initial = super(ChildCreateView, self).get_initial()
        pk = self.kwargs.get('pk')
        initial['parent'] = get_object_or_404(Parent, pk=pk)
        return initial

    def form_valid(self, form):
        messages.success(self.request, '{}'.format('Registered! We\'ll contact you soon'))
        return super(ChildCreateView, self).form_valid(form)


class ChildDetailView(DetailView):
    queryset = Child.objects.all()
    template_name = 'child-detail-view.html'
    permission_required = 'NurseryApp.view_child'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        child_day_of_birth = Child.objects.get(pk=self.kwargs.get('pk')).day_of_birth
        now = datetime.date.today()
        rd = relativedelta(now, child_day_of_birth)
        if rd.years == 0:
            months = '{} months'.format(rd.months)
        else:
            months = '{} year(s), {} month(s)'.format(rd.years, rd.months)
        context['months'] = months
        return context


class ChildUpdateView(PermissionRequiredMixin, UpdateView):
    queryset = Child.objects.all()
    form_class = ChildCreateForm
    template_name = 'child-update-view.html'
    permission_required = 'NurseryApp.change_child'

    def form_valid(self, form):
        messages.success(self.request, '{}'.format('Updated child data!'))
        return super(ChildUpdateView, self).form_valid(form)


class ChildDeleteView(PermissionRequiredMixin, DeleteView):
    model = Child
    template_name = 'child-delete-view.html'
    success_url = reverse_lazy('main-view')
    permission_required = 'NurseryApp.delete_child'


class ChildListView(PermissionRequiredMixin, ListView):
    queryset = Child.objects.all().order_by('-status')
    template_name = 'child-list-view.html'
    paginate_by = 6
    permission_required = 'NurseryApp.view_group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all().order_by('pk')
        context['groups'] = groups
        return context


class GroupCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'group-create-view.html'
    form_class = GroupCreateForm
    success_url = reverse_lazy('group-list-view')
    permission_required = 'NurseryApp.add_group'


class GroupDetailView(PermissionRequiredMixin, DetailView):
    queryset = Group.objects.all()
    template_name = 'group-detail-view.html'
    permission_required = 'NurseryApp.view_group'


class GroupUpdateView(PermissionRequiredMixin, UpdateView):
    queryset = Group.objects.all()
    form_class = GroupCreateForm
    template_name = 'group-update-view.html'
    success_url = reverse_lazy('group-list-view')
    permission_required = 'NurseryApp.change_group'


class GroupDeleteView(PermissionRequiredMixin, DeleteView):
    model = Group
    template_name = 'group-delete-view.html'
    success_url = reverse_lazy('group-list-view')
    permission_required = 'NurseryApp.delete_group'


class GroupListView(PermissionRequiredMixin, ListView):
    queryset = Group.objects.all().order_by('pk')
    template_name = 'group-list-view.html'
    permission_required = 'NurseryApp.view_group'
    paginate_by = 8



class TeacherCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'teacher-create-view.html'
    form_class = TeacherCreateForm
    success_url = reverse_lazy('teacher-list-view')
    permission_required = 'NurseryApp.add_teacher'


class TeacherDetailView(PermissionRequiredMixin, DetailView):
    queryset = Teacher.objects.all()
    template_name = 'teacher-detail-view.html'
    permission_required = 'NurseryApp.view_teacher'


class TeacherUpdateView(PermissionRequiredMixin, UpdateView):
    queryset = Teacher.objects.all()
    form_class = TeacherCreateForm
    template_name = 'teacher-update-view.html'
    success_url = reverse_lazy('teacher-list-view')
    permission_required = 'NurseryApp.change_teacher'


class TeacherDeleteView(PermissionRequiredMixin, DeleteView):
    model = Teacher
    template_name = 'teacher-delete-view.html'
    success_url = reverse_lazy('teacher-list-view')
    permission_required = 'NurseryApp.delete_teacher'


class TeacherListView(PermissionRequiredMixin, ListView):
    queryset = Teacher.objects.all().order_by('group__name')
    template_name = 'teacher-list-view.html'
    permission_required = 'NurseryApp.view_teacher'
    paginate_by = 8



class CaregiverCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'caregiver-create-view.html'
    form_class = CaregiverCreateForm
    permission_required = 'NurseryApp.add_caregiver'

    def get_initial(self):
        initial = super(CaregiverCreateView, self).get_initial()
        pk = self.kwargs.get('pk')
        initial['parent'] = get_object_or_404(Parent, pk=pk)
        return initial

    def form_valid(self, form):
        messages.success(self.request, '{}'.format('Added Caregiver!'))
        return super(CaregiverCreateView, self).form_valid(form)


class CaregiverDetailView(PermissionRequiredMixin, DetailView):
    queryset = Caregiver.objects.all()
    template_name = 'caregiver-detail-view.html'
    permission_required = 'NurseryApp.view_caregiver'


class CaregiverUpdateView(PermissionRequiredMixin, UpdateView):
    queryset = Caregiver.objects.all()
    form_class = CaregiverCreateForm
    template_name = 'caregiver-update-view.html'
    permission_required = 'NurseryApp.change_caregiver'


class CaregiverDeleteView(PermissionRequiredMixin, DeleteView):
    model = Caregiver
    template_name = 'caregiver-delete-view.html'
    success_url = reverse_lazy('main-view')
    permission_required = 'NurseryApp.delete_caregiver'


class ActivityCreateView(PermissionRequiredMixin, CreateView):
    queryset = Activity.objects.all()
    form_class = ActivityCreateForm
    template_name = 'activity-create-view.html'
    permission_required = 'NurseryApp.add_activity'


class ActivityDetailView(PermissionRequiredMixin, DetailView):
    queryset = Activity.objects.all()
    template_name = 'activity-detail-view.html'
    permission_required = 'NurseryApp.view_activity'


class ActivityUpdateView(PermissionRequiredMixin, UpdateView):
    queryset = Activity.objects.all()
    form_class = ActivityCreateForm
    permission_required = 'NurseryApp.change_activity'


class ActivityDeleteView(PermissionRequiredMixin, DeleteView):
    model = Activity
    template_name = 'activity-delete-view.html'
    success_url = reverse_lazy('main-view')
    permission_required = 'NurseryApp.delete_activity'


class ActivityListView(PermissionRequiredMixin, ListView):
    queryset = Activity.objects.all()
    template_name = 'activity-list-view.html'
    permission_required = 'NurseryApp.view_activity'
    paginate_by = 8


class DietCreateView(PermissionRequiredMixin, CreateView):
    queryset = Diet.objects.all()
    form_class = DietCreateForm
    template_name = 'diet-create-view.html'
    permission_required = 'NurseryApp.add_diet'


class DietDetailView(PermissionRequiredMixin, DetailView):
    queryset = Diet.objects.all()
    template_name = 'diet-detail-view.html'
    permission_required = 'NurseryApp.view_diet'


class DietUpdateView(PermissionRequiredMixin, UpdateView):
    queryset = Diet.objects.all()
    form_class = DietCreateForm
    template_name = 'diet-update-view.html'
    permission_required = 'NurseryApp.change_diet'


class DietDeleteView(PermissionRequiredMixin, DeleteView):
    model = Diet
    template_name = 'diet-delete-view.html'
    success_url = reverse_lazy('main-view')
    permission_required = 'NurseryApp.delete_diet'


class DietListView(PermissionRequiredMixin, ListView):
    queryset = Diet.objects.all()
    template_name = 'diet-list-view.html'
    permission_required = 'NurseryApp.view_diet'
    paginate_by = 8



class VerifyChildView(View):
    def get(self, request, pk):
        child = Child.objects.get(pk=pk)
        children = Child.objects.all().filter(status='2').count()
        if child.status == '1':
            child.status = '2'
        child.save()
        messages.success(request, '{}'.format('Changed child\'s status on \'Waiting\''))
        return render(request, 'verify-child-view.html', {'child': child,
                                                          'children': children})


class AddingChildToGroupView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        child = Child.objects.get(pk=pk)
        form = AddingChildToGroupForm(initial={'child': child})
        return render(request, 'child-add-group-view.html', {'form': form,
                                                             'child': child})

    def post(self, request, pk):
        form = AddingChildToGroupForm(request.POST or None)
        ctx = {
            'form': form
        }
        if form.is_valid():
            child = Child.objects.get(pk=pk)
            group = form.cleaned_data['group']
            group_object = Group.objects.get(name=group)
            if group_object.child_set.all().count() >= group_object.max_capacity:
                messages.success(request, 'This group if full, pick another one')
                return redirect(reverse_lazy('child-list-view'))
            group_object.child_set.add(child)
            child.status = '3'
            child.save()
            group_object.save()
            return redirect(reverse_lazy('child-list-view'))
        return render(request, 'child-add-group-view.html', ctx)


class AddingTeacherToGroupView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        teacher = Teacher.objects.get(pk=pk)
        form = AddingTeacherToGroupForm(initial={'teacher': teacher})
        ctx = {
            'form': form,
            'teacher': teacher
        }
        return render(request, 'teacher-add-group-view.html', ctx)

    def post(self, request, pk):
        form = AddingTeacherToGroupForm(request.POST or None)
        if form.is_valid():
            teacher = Teacher.objects.get(pk=pk)
            group = form.cleaned_data['group']
            group_object = Group.objects.get(name=group)
            group_object.teacher_set.add(teacher)
            teacher.save()
            group_object.save()
            return redirect(reverse_lazy('teacher-list-view'))
        return render(request, 'teacher-add-group-view.html', {'form': form})


class ParentListView(PermissionRequiredMixin, ListView):
    queryset = Parent.objects.all()
    template_name = 'parent-list-view.html'
    permission_required = 'NurseryApp.view_parent'


class SetParentNotActive(View):
    def get(self, request):
        not_active_parents = Parent.objects.all().filter(child=None)
        object_list = Parent.objects.all()
        for parent in not_active_parents:
            parent.active = False
            parent.save()
        messages.success(request, '{}'.format('Set \'INACTIVE\' status for users without registered children'))
        return render(request, 'parent-list-view.html', {'object_list': object_list})

# class MessageCreateView(CreateView):
#     form_class = MessageCreateForm
#     template_name = 'message-create-view.html'
#
#     def get_initial(self):
#         initial = super(MessageCreateView, self).get_initial()
#         sender_pk = self.kwargs.get('sender_pk')
#         receiver_pk = self.kwargs.get('receiver_pk')
#         initial['sender'] = User.objects.get(pk=sender_pk)
#         initial['receiver'] = User.objects.get(pk=receiver_pk)
#         return initial
