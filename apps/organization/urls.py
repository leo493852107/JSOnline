#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import OrgView, AddUserAskView, OrganizationHomeView, OrganizationCourseView, OrganizationDescView, OrganizationTeacherView, AddFavView, TeacherListView, TeacherDetailView


urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrganizationHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrganizationCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrganizationDescView.as_view(), name="org_desc"),
    url(r'^teacher/(?P<org_id>\d+)/$', OrganizationTeacherView.as_view(), name="org_teacher"),


    # 机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    # 讲师列表页
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),

    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]
