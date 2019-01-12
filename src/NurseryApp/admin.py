from django.contrib import admin
from .models import Parent, Child, Group, Teacher, Caregiver, Activity, Diet, Message

admin.site.register(Parent)
admin.site.register(Child)
admin.site.register(Group)
admin.site.register(Teacher)
admin.site.register(Caregiver)
admin.site.register(Activity)
admin.site.register(Diet)
admin.site.register(Message)

