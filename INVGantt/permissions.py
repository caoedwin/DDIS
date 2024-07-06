from rest_framework.permissions import BasePermission
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import Group, User
from app01.models import UserInfo,Role
class MyPermission(BasePermission):
    def has_permission(self, request, view):
        # # 只读接口判断
        # r1 = request.method in ('GET', 'HEAD', 'OPTIONS')
        # # group为有权限的分组
        # group = Group.objects.filter(name='管理员').first()
        # # groups为当前用户所属的所有分组
        # groups = request.user.groups.all()
        # r2 = group and groups
        # r3 = group in groups
        # # 读接口大家都有权限，写接口必须为指定分组下的登陆用户
        # return r1 or (r2 and r3)

        # 只读接口判断
        # print(request.method)
        # print(request.GET)
        # print(request.POST)
        # print(request.data)
        # print(request.query_params)
        # print(request.user)
        print(request, request.method, request.user)
        r1 = request.method in ('GET', 'HEAD', 'OPTIONS')
        # group为有权限的分组
        # group = Role.objects.all()
        # group = UserInfo.objects.filter(account="C1010S3").first().role.all()
        group = Role.objects.filter(name="admin").first()
        print(group)
        # groups为当前用户所属的所有分组
        if str(request.user) == "AnonymousUser" or not request.user:
            # print(1)
            groups = []
            # return redirect('/login/')
        else:
            groups = request.user.role.all()
        print(group,groups)
        r2 = group and groups
        r3 = group in groups
        print(r1,r2,r3)
        # 读接口大家都有权限，写接口必须为指定分组下的登陆用户
        print(r1 or (r2 and r3))
        # return r1 or (r2 and r3)
        return r2 and r3

# from rest_framework.permissions import BasePermission
# from django.contrib.auth.models import Group,User
# class MyPermission(BasePermission):
#     def has_permission(self, request, view):
#         # 只读接口判断
#         print(request, request.method, request.user)
#         r1 = request.method in ('GET', 'HEAD', 'OPTIONS')
#         # group为有权限的分组
#         group = Group.objects.filter(name='Managers').first()
#         r4 = request.user.is_staff
#         print(request.user.is_staff)#(职员状态打勾的才有权限)
#         # groups为当前用户所属的所有分组
#         groups = request.user.groups.all()
#         print(group, groups)
#         r2 = group and groups
#         r3 = group in groups
#         print(r1, r4, r2, r3)
#         # 读接口大家都有权限，写接口必须为指定分组下的登陆用户
#         # return r1 or (r2 and r3)
#         return r4 or (r2 and r3)