# -*- coding:utf-8-*-
# @Author : PeterYang
# @Email : snfnvtk@163.com
# @Time : 2019/5/30
# @Site : 
# @File : UserAuthMiddleware.py
# @Software : PyCharm


# from django.http import HttpResponseRedirect
# from django.utils.deprecation import MiddlewareMixin
# from apps.account.models import
# from datetime import datetime
# from django.shortcuts import render, reverse, redirect
#
#
# class UserLoginMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.path == "/account/login/":
#             return None
#         else:
#             ticket = request.COOKIES.get('ticket')
#             if not ticket:
#                 return redirect("/account/login/")
#             user_ticket = UserTicketModel.objects.filter(ticket=ticket)
#             if user_ticket:
#                 # 判断令牌是否有效,无效则删除
#                 out_time = user_ticket[0].out_time.replace(tzinfo=None)
#                 now_time = datetime.utcnow()
#
#                 if out_time > now_time:
#                     # 没有失效
#                     request.user = user_ticket[0].user
#                 else:
#                     user_ticket.delete()