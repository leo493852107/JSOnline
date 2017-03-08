#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import CourseOrganization, City


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

        #
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
