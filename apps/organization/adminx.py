#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import City, CourseOrganization, Teacher


import xadmin


class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrganizationAdmin(object):
    list_display = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'add_time']
    search_fields = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address']
    list_filter = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'add_time']

    # 设置外键为搜索模式
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['organization', 'name', 'work_years', 'work_company', 'work_position', 'work_position', 'points', 'click_num', 'fav_num', 'add_time']
    search_fields = ['organization', 'name', 'work_years', 'work_company', 'work_position', 'work_position', 'points', 'click_num', 'fav_num']
    list_filter = ['organization', 'name', 'work_years', 'work_company', 'work_position', 'work_position', 'points', 'click_num', 'fav_num', 'add_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrganization, CourseOrganizationAdmin)
xadmin.site.register(Teacher, TeacherAdmin)


