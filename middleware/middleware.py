from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from app.models import AXFUser
from app.views_constant import NOT_LOGIN

REQUIRE_LOGIN_JSON = [
    '/app/addtocart/',
    '/app/subtocart/',
    '/app/allselect/',
    '/app/changecartstate/',
    '/app/makeorder/',
    '/app/payed/',
    '/app/received/',
]

REQUIRE_LOGIN=[
    '/app/cart/',
    '/app/mine/',
    'app/allorderlist/',
    '/app/orderlistnotpay/',
    '/app/orderlistnotreceive/',
    '/app/addresslist/',
]

class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path in REQUIRE_LOGIN_JSON:
            token = request.GET.get('token')
            user_id = cache.get(token)
            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    request.user = user#给reqeust增加一个属性值user,需要使用时直接获取
                except:
                    data = {
                        'status': 302,
                        'msg': '用户id失效'
                    }
                    return JsonResponse(data=data)
            else:
                data = {
                    'status': NOT_LOGIN,
                    'msg': '未登陆，请重新登陆',
                }
                return JsonResponse(data=data)
        if request.path in REQUIRE_LOGIN:
            token = request.GET.get('token')
            user_id = cache.get(token)
            if user_id:
                try:
                    user=AXFUser.objects.get(pk=user_id)
                    request.user=user#给reqeust增加一个属性值user,需要使用时直接获取
                except:
                    return redirect(reverse('app:login'))
            else:
                return redirect(reverse('app:login'))
