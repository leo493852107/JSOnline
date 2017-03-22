#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Course, Lesson, Video, CourseResource, BannerCourse

import xadmin


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num', 'add_time']
    # 根据点击数倒序排列
    ordering = ['-click_num']

    # 设置只读
    # readonly_fields = ['click_num', 'fav_nums']
    readonly_fields = ['fav_nums']

    # 设置页面不显示
    exclude = ['click_num']

    # 页面组装
    inlines = [LessonInline, CourseResourceInline]

    # 轮播图的过滤 NO
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs


class BannnerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_num', 'add_time']
    # 根据点击数倒序排列
    ordering = ['-click_num']

    # 设置只读
    # readonly_fields = ['click_num', 'fav_nums']
    readonly_fields = ['fav_nums']

    # 设置页面不显示
    exclude = ['click_num']

    # 页面组装
    inlines = [LessonInline, CourseResourceInline]

    # 轮播图的过滤 YES
    def queryset(self):
        qs = super(BannnerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannnerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)


