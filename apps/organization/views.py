#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import CourseOrganization, City, Teacher
from .forms import UserAskForm
from course.models import Course
from operation.models import UserFavorite


# Create your views here.


class OrgView(View):
    '''
    课程机构列表功能
    '''
    def get(self, request):
        # 课程机构
        all_organizations = CourseOrganization.objects.all()

        hot_organizations = all_organizations.order_by("-click_num")[:3]

        # 城市
        all_cities = City.objects.all()

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_organizations = all_organizations.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_organizations = all_organizations.filter(category=category)


        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_organizations = all_organizations.order_by("-students")
            elif sort == "courses":
                all_organizations = all_organizations.order_by("-course_nums")


        organization_nums = all_organizations.count()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_organizations, 5, request=request)

        organizations = p.page(page)


        return render(request, "org-list.html", {
            "all_organizations": organizations,
            "all_cities": all_cities,
            "organization_nums": organization_nums,
            "city_id": city_id,
            "category": category,
            "hot_organizations": hot_organizations,
            "sort": sort,

        })


class AddUserAskView(View):
    '''
    用户添加咨询
    '''
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():

            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加出错"}', content_type='application/json')


class OrganizationHomeView(View):
    '''
    机构首页
    '''
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrganization.objects.get(id=int(org_id))
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            # 课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        # 通过外键反向取出所有课程
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrganizationCourseView(View):
    '''
    机构课程列表页
    '''
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrganization.objects.get(id=int(org_id))
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            # 课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 通过外键反向取出所有课程
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrganizationDescView(View):
    '''
    机构介绍页
    '''
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrganization.objects.get(id=int(org_id))
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            # 课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrganizationTeacherView(View):
    '''
    机构讲师页
    '''
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrganization.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        # 判断是否收藏
        has_fav = False
        if request.user.is_authenticated():
            # 课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class AddFavView(View):
    '''
    用户收藏
    '''
    def post(self, request):
        # 数据id
        fav_id = request.POST.get('fav_id', 0)
        # 1.课程 2.课程机构 3.讲师
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登录
        if not request.user.is_authenticated():
            # 未登录
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type="application/json")

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        # 已收藏, 取消
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type="application/json")
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type="application/json")


class TeacherListView(View):
    '''
    课程讲师列表页
    '''
    def get(self, request):
        all_teachers = Teacher.objects.all()

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by("-click_num")

        sorted_teachers = Teacher.objects.all().order_by("-click_num")[:3]

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            'all_teachers': teachers,
            'sorted_teachers': sorted_teachers,
            'sort': sort

        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_num += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.organization.id):
            has_org_faved = True

        # 讲师排行
        sorted_teacher = Teacher.objects.all().order_by("-click_num")[:3]
        return render(request, "teacher-detail.html", {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teacher': sorted_teacher,
            'has_teacher_faved': has_teacher_faved,
            'has_org_faved': has_org_faved,


        })
