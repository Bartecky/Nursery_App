from django.contrib import admin
from .models import Parent, Child, Group, Teacher, Caregiver

admin.site.register(Parent)
admin.site.register(Child)
admin.site.register(Group)
admin.site.register(Teacher)
admin.site.register(Caregiver)
