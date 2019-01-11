from django import forms
from django.contrib.auth.models import User
from .models import Child, Parent, Group, Teacher, Caregiver, Activity, Diet
from django.core.validators import EmailValidator
import datetime


class SignupUserForm(forms.Form):
    username = forms.CharField(max_length=64)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    email = forms.EmailField(validators=[EmailValidator])

    def clean(self):
        data = self.cleaned_data
        if data['password'] != data['confirm_password']:
            raise forms.ValidationError('passwords are not the same')
        return data


class ChildCreateForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Parent.objects.all(), widget=forms.HiddenInput)
    year = datetime.date.today().year
    day_of_birth = forms.DateField(widget=forms.SelectDateWidget(
        years=[x for x in range(year - 4, year)]
    ))
    diet = forms.ModelMultipleChoiceField(queryset=Diet.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    activity = forms.ModelMultipleChoiceField(queryset=Activity.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        model = Child
        fields = [
            'parent',
            'first_name',
            'last_name',
            'sex',
            'day_of_birth',
            'diet',
            'activity'
        ]


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = [
            'name',
            'description',
            'max_capacity'
        ]


class TeacherCreateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
        ]

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) != 9:
            raise forms.ValidationError('Number must be nine-digit')
        return phone


class CaregiverCreateForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Parent.objects.all(), widget=forms.HiddenInput)

    class Meta:
        model = Caregiver
        fields = [
            'parent',
            'first_name',
            'last_name',
            'phone',
            'email',
            'relationship_with_child'
        ]

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) != 9:
            raise forms.ValidationError('Number must be nine-digit')
        return phone


class ActivityCreateForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'name',
            'description'
        ]


class DietCreateForm(forms.ModelForm):
    class Meta:
        model = Diet
        fields = [
            'name',
            'description'
        ]


class AddingChildToGroupForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all().order_by('pk'))
    child = forms.ModelChoiceField(queryset=Child.objects.all(), widget=forms.HiddenInput)


class AddingTeacherToGroupForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all().order_by('pk'))
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), widget=forms.HiddenInput)


# class MessageCreateForm(forms.ModelForm):
#     sender = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
#     receiver = forms.ModelChoiceField(queryset=User.objects.all())
#     class Meta:
#         model = Message
#         fields = [
#             'sender',
#             'receiver',
#             'subject',
#             'content',
#         ]