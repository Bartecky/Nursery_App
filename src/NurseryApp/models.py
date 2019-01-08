from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


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
    group = models.ForeignKey('Group', blank=True, null=True, on_delete=models.CASCADE)
    day_of_birth = models.DateField()



    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name_plural = 'children'
        ordering = ['last_name']


class Group(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()




# Group
# Teacher
# Waiting list?
# Activity
# Caregiver



