"""Nursery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from NurseryApp.views import (
    NurseryLoginView,
    NurseryLogoutView,
    SignupView,
    MainPageView,
    ChildCreateView,
    ChildDetailView,
    ChildUpdateView,
    ChildDeleteView,
    ChildListView,
    GroupCreateView,
    GroupDetailView,
    GroupUpdateView,
    GroupDeleteView,
    GroupListView,
    TeacherCreateView,
    TeacherDetailView,
    TeacherUpdateView,
    TeacherDeleteView,
    TeacherListView,
    CaregiverCreateView,
    CaregiverDetailView,
    CaregiverUpdateView,
    CaregiverDeleteView,
    ActivityCreateView,
    ActivityDetailView,
    ActivityUpdateView,
    ActivityDeleteView,
    ActivityListView,
    DietCreateView,
    DietDetailView,
    DietUpdateView,
    DietDeleteView,
    DietListView,
    # WaitingListView
)

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^$', NurseryLoginView.as_view(), name='login-view'),
    url(r'^logout/$', NurseryLogoutView.as_view(), name='logout-view'),
    url(r'^signup/$', SignupView.as_view(), name='signup-view'),
    url(r'^main/$', MainPageView.as_view(), name='main-view'),
    #
    url(r'^parent/(?P<pk>(\d)+)/add_child/$', ChildCreateView.as_view(), name='child-create-view'),
    url(r'^child/detail/(?P<pk>(\d)+)/$', ChildDetailView.as_view(), name='child-detail-view'),
    url(r'^child/update/(?P<pk>(\d)+)/$', ChildUpdateView.as_view(), name='child-update-view'),
    url(r'^child/delete/(?P<pk>(\d)+)/$', ChildDeleteView.as_view(), name='child-delete-view'),
    url(r'^child_list/$', ChildListView.as_view(), name='child-list-view'),
    url(r'^add_group/$', GroupCreateView.as_view(), name='group-create-view'),
    url(r'^group/detail/(?P<pk>(\d)+)/$', GroupDetailView.as_view(), name='group-detail-view'),
    url(r'^group/update/(?P<pk>(\d)+)/$', GroupUpdateView.as_view(), name='group-update-view'),
    url(r'^group/delete/(?P<pk>(\d)+)/$', GroupDeleteView.as_view(), name='group-delete-view'),
    url(r'^group/list/$', GroupListView.as_view(), name='group-list-view'),
    url(r'^add_teacher/$', TeacherCreateView.as_view(), name='teacher-create-view'),
    url(r'^teacher/detail/(?P<pk>(\d)+)/$', TeacherDetailView.as_view(), name='teacher-detail-view'),
    url(r'^teacher/update/(?P<pk>(\d)+)/$', TeacherUpdateView.as_view(), name='teacher-update-view'),
    url(r'^teacher/delete/(?P<pk>(\d)+)/$', TeacherDeleteView.as_view(), name='teacher-delete-view'),
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher-list-view'),
    url(r'^parent/(?P<pk>(\d)+)/add_caregiver/$', CaregiverCreateView.as_view(), name='caregiver-create-view'),
    url(r'^caregiver/detail/(?P<pk>(\d)+)/$', CaregiverDetailView.as_view(), name='caregiver-detail-view'),
    url(r'^caregiver/update/(?P<pk>(\d)+)/$', CaregiverUpdateView.as_view(), name='caregiver-update-view'),
    url(r'^caregiver/delete/(?P<pk>(\d)+)/$', CaregiverDeleteView.as_view(), name='caregiver-delete-view'),
    url(r'^add_activity/$', ActivityCreateView.as_view(), name='activity-create-view'),
    url(r'^activity/detail/(?P<pk>(\d)+)/$', ActivityDetailView.as_view(), name='activity-detail-view'),
    url(r'^activity/update/(?P<pk>(\d)+)/$', ActivityUpdateView.as_view(), name='activity-update-view'),
    url(r'^activity/delete/(?P<pk>(\d)+)/$', ActivityDeleteView.as_view(), name='activity-delete-view'),
    url(r'^activity/list/$', ActivityListView.as_view(), name='activity-list-view'),
    url(r'^add_diet/$', DietCreateView.as_view(), name='diet-create-view'),
    url(r'^diet/detail/(?P<pk>(\d)+)/$', DietDetailView.as_view(), name='diet-detail-view'),
    url(r'^diet/update/(?P<pk>(\d)+)/$', DietUpdateView.as_view(), name='diet-update-view'),
    url(r'^diet/delete/(?P<pk>(\d)+)/$', DietDeleteView.as_view(), name='diet-delete-view'),
    url(r'^diet/list/$', DietListView.as_view(), name='diet-list-view'),
    # url(r'^waiting_list/$', WaitingListView.as_view(), name='waiting-list-view')


]
