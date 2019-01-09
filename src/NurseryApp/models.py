from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy


# Create your models here.
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=9, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    day_of_birth = models.DateField()
    group = models.ForeignKey('Group', blank=True, null=True, on_delete=models.CASCADE)
    activity = models.ManyToManyField('Activity', blank=True, null=True)
    diet = models.ManyToManyField('Diet', blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse_lazy('child-detail-view', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'children'
        ordering = ['last_name']


class Group(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    # max_capacity

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=9, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    group = models.ForeignKey(Group, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Caregiver(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=9, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    relationship_with_child = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse_lazy('caregiver-detail-view', kwargs={'pk': self.pk})


class Activity(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('activity-detail-view', kwargs={'pk': self.pk})

    class Meta:
        verbose_name_plural = 'Activities'



class Diet(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('diet-detail-view', kwargs={'pk': self.pk})


class Waiting_list(models.Model):
    child = models.ManyToManyField(Child)
    group = models.ManyToManyField(Group)