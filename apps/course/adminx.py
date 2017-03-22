#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organization.models import CourseOrganization

import xadmin


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'add_time', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'add_time']
    # 根据点击数倒序排列
    ordering = ['-click_num']

    # 设置只读
    # readonly_fields = ['click_num', 'fav_nums']
    readonly_fields = ['fav_nums']

    # 在列表页直接修改
    list_editable = ['degree', 'desc']

    # 设置页面不显示
    exclude = ['click_num']

    # 页面组装
    inlines = [LessonInline, CourseResourceInline]

    # 指明 detail 字段使用 ueditor 样式
    style_fields = {"detail": "ueditor"}

    # 会覆盖自定义excel插件 (支持导入excel)
    import_excel = True

    # 刷新时间 可选
    # refresh_times = [3, 5, 10]

    # 轮播图的过滤 NO
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    # 在保存课程的时候，统计课程机构数量
    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)



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


