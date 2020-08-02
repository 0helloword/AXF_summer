import json
import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from AXF.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT, MEDIA_KEY_PREFIX
from app.models import MainWheel, MainNav, MainMustbuy, MainShop, MainShow, FoodType, Goods, AXFUser, Cart, Order, \
    OrderGoods, Address
from app.view_helper import get_total_price

from app.views_constant import ALL_TYPE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN, \
    HTTP_OK, HTTP_USER_EXIST, HTTP_EMAIL_EXIST, PASSWORD_NOT_MATCH, HTTP_USERINFO_ERROR, NOT_LOGIN, \
    ORDER_STATUS_NO_SEND, ORDER_STATUS_NO_PAY, ORDER_STATUS_NO_RECEIVE, ORDER_STATUS_NO_COMMENT


# home页面，主要是读取数据
def home(request):
    mainwheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_mustbuys = MainMustbuy.objects.all()
    main_shops = MainShop.objects.all()
    main_shop0_1 = main_shops[0:1]
    main_shops1_3 = main_shops[1:3]
    main_shop3_7 = main_shops[3:7]
    main_shop7_11 = main_shops[7:11]
    main_shows = MainShow.objects.all()
    data = {
        'title': '首页',
        'main_wheels': mainwheels,
        'main_navs': main_navs,
        'main_mustbuys': main_mustbuys,
        'main_shop0_1': main_shop0_1,
        'main_shops1_3': main_shops1_3,
        'main_shop3_7': main_shop3_7,
        'main_shop7_11': main_shop7_11,
        'main_shows': main_shows,
    }
    return render(request, 'main/home.html', context=data)


# 闪购页面，展示所有的商品，并实现对应的筛选
def market(request):
    return redirect(reverse('app:marketwithparams', kwargs={
        "typeid": 104749,
        "childcid": 0,
        "order_rule": 0,
    }))


def marketwithparams(request, typeid, childcid, order_rule):
    foodtypes = FoodType.objects.all()
    goods_list = Goods.objects.filter(categoryid=typeid)
    if childcid == ALL_TYPE:
        pass
    else:
        goods_list = goods_list.filter(childcid=childcid)
    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        goods_list = goods_list.order_by("price")
    elif order_rule == ORDER_PRICE_DOWN:
        goods_list = goods_list.order_by("-price")
    elif order_rule == ORDER_SALE_UP:
        goods_list = goods_list.order_by("productnum")
    elif order_rule == ORDER_SALE_DOWN:
        goods_list = goods_list.order_by("-productnum")

    order_rule_list = [['综合排序', ORDER_TOTAL], ['价格升序', ORDER_PRICE_UP], ['价格降序', ORDER_PRICE_DOWN],
                       ['销量升序', ORDER_SALE_UP], ['销量降序', ORDER_SALE_DOWN]
                       ]
    foodtype = foodtypes.get(typeid=typeid)
    foodchildtype = foodtype.childtypenames
    foodchildtype_list = foodchildtype.split('#')
    foodtype_childname_list = []
    for i in foodchildtype_list:
        foodtype_childname_list.append(i.split(':'))
    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'order_rule_list': order_rule_list,
        'foodtype_childname_list': foodtype_childname_list,
        'typeid': int(typeid),
        'childcid': int(childcid),
        'order_rule': order_rule,
    }
    return render(request, 'main/market.html', context=data)


'''
购物车页面，获取购物车商品数据
提供默认的收货地址
js实现：
1.对购物车的商品数量进行增减
2.选中，取消选中某个商品
3.全选功能
'''


def cart(request):
    carts = Cart.objects.filter(c_user_id=request.user).filter(c_goods_num__gt=0)
    address = Address.objects.filter(a_user_id=request.user)
    address = address.first()
    context = {
        'carts': carts,
        'address': address,
    }
    return render(request, 'main/cart.html', context=context)


'''
加购商品
如购物车中已有该用户及该商品的记录，则商品数量+1
如购物车中无该商品的记录，则新增一条商品记录
'''


def addtocart(request):
    print(request.user)
    goodsid = request.GET.get("goodsid")
    carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)
    if carts.exists():  # 如果购物车中有该商品记录
        cart = carts.first()
        cart.c_goods_num = cart.c_goods_num + 1
    else:
        cart = Cart()  # 无该商品记录
        cart.c_user_id = request.user.id
        cart.c_goods_id = goodsid
        cart.c_goods_num = 1
    cart.save()
    data = {
        'status': 200,
        'msg': '添加成功',
        'good_num': cart.c_goods_num,
        'total_price': get_total_price(request.user)
    }
    return JsonResponse(data=data)


'''
减少商品数量
如购物车中已有该用户及该商品的记录，则商品数量-1
如购物车中商品数量为0，则将该商品记录在数据库删掉
'''


def subtocart(request):
    goodid = request.GET.get('goodsid')
    carts = Cart.objects.filter(c_user_id=request.user.id).filter(c_goods_id=goodid)
    data = {
        'status': 200,
        'good_num': 0
    }
    if carts.exists():
        cart = carts.first()
        if cart.c_goods_num > 1:
            cart.c_goods_num = cart.c_goods_num - 1
            data['good_num'] = cart.c_goods_num
            cart.save()
            data['total_price'] = get_total_price(request.user)
            return JsonResponse(data=data)
        else:
            cart.delete()  # 减为0则在数据库删除该条数据
            data['good_num'] = 0
            data['total_price'] = 0
            return JsonResponse(data=data)
    return JsonResponse(data=data)


@csrf_exempt
def mine(request):
    data = {
        'title': '我的',
        'is_login': False
    }
    user = AXFUser.objects.get(pk=request.user.id)
    data['is_login'] = True
    data['username'] = user.u_username
    data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url
    data['order_not_pay'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NO_PAY).count()
    data['order_not_recive'] = Order.objects.filter(o_user=user).filter(
        o_status__in=[ORDER_STATUS_NO_RECEIVE, ORDER_STATUS_NO_SEND]).count()
    data['order_not_comment'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NO_COMMENT).count()
    return render(request, 'main/mine.html', context=data)


'''
注册功能：
1.使用了django自带的密码加密方法
2.图片文件的上传
3.注册成功后使用异步处理方式发送激活邮件到用户邮箱
使用js实现了：
1.必填字段的非空判断
2.用户名，邮箱的唯一性校验
3.密码和确认密码的一致性校验
'''


def register(request):
    if request.method == 'GET':  # get请求展示注册页面
        return render(request, 'user/register.html')
    elif request.method == 'POST':  # post请求提交注册的用户数据
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = make_password(password)  # 使用django系统自带的加密方法加密密码
        icon = request.FILES.get('icon')  # 文件获取使用FILES方法
        user = AXFUser()
        user.u_username = username
        user.u_password = password
        user.u_email = email
        user.u_icon = icon
        user.save()
        u_token = uuid.uuid4().hex  # 生成token给激活链接使用
        cache.set(u_token, user.id, timeout=60 * 60 * 2)  # 使用redis缓存，一般需要根据token找userid,所以token要放在前面
        # from app.view_helper import send_email  #这里调用的是未做异步处理的发送邮件方法
        # send_email(email,username,u_token)#这里发送邮件未做异步处理，需要等邮件发送出去才会跳转到登陆页面
        from app.tasks import send_email
        send_email.delay(email, username, u_token)  # 使用celery进行异步处理邮件发送
        # return redirect(reverse('app:login'))
        return render(request, 'user/login.html')


'''
登陆
实现：
1.使用系统自带的校验密码方法校验用户的密码
2.使用前后端分离方式返回登陆的校验结果，前端根据状态码判断页面跳转
前端使用js实现了：
1.必填字段的非空判断
2.将登陆接口返回的token进行本地保存
'''


@csrf_exempt
def login(request):
    if request.method == 'GET':  # get请求返回登陆页面
        return render(request, 'user/login.html')
    elif request.method == 'POST':  # post请求返回用户身份校验结果
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        users = AXFUser.objects.filter(u_username=username)
        if users.exists():
            user = users.first()
            token = uuid.uuid4().hex
            checkpassword = check_password(password, user.u_password)  # 使用系统自带的校验密码方法，前端输入的密码放在前面
            print(checkpassword)
            if checkpassword:
                cache.set(token, user.id, timeout=60 * 60 * 2)  # 使用redis缓存，一般需要根据token找userid,所以token要放在前面
                data = {
                    "status": 200,
                    "msg": "success",
                    "token": token
                }
                return JsonResponse(data=data)
        data = {
            "status": 701,
            "msg": "fail"
        }
        return JsonResponse(data=data)


# 用户激活
def active(request):
    token = request.GET.get('u_token')
    user_id = cache.get(token)
    print(token, user_id)
    if user_id:
        cache.delete(token)  # 使激活码链接只能使用一次
        user = AXFUser.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        return render(request, 'user/login.html')
    return render(request, 'user/active_fail.html')


# 配合注册时js的用户名唯一性校验
def checkuser(request):
    username = request.GET.get('username')
    users = AXFUser.objects.filter(u_username=username)
    data = {
        'status': HTTP_OK,
        'msg': '用户名可使用',
    }
    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = '用户名已存在'
    else:
        pass
    return JsonResponse(data=data)


# 配合注册时js的邮箱唯一性校验
def checkemail(request):
    email = request.GET.get('email')
    users = AXFUser.objects.filter(u_email=email)
    data = {
        'status': HTTP_OK,
        'msg': '邮箱可使用',
    }
    if users.exists():
        data['status'] = HTTP_EMAIL_EXIST
        data['msg'] = '邮箱已存在'
    else:
        pass
    return JsonResponse(data=data)


# 配合注册时js的密码和确认密码的一致性校验
def checkpassword(request):
    pwd = request.GET.get('password')
    pwd_confirm = request.GET.get('password_confirm')
    data = {
        'status': HTTP_OK,
        'msg': 'ok',
    }
    if pwd != pwd_confirm:
        data['status'] = PASSWORD_NOT_MATCH
        data['msg'] = '两次密码不一致'
    else:
        pass
    return JsonResponse(data=data)


# 全选按钮
def allselect(request):
    cart_list = request.GET.get('cart_list')
    print(cart_list)
    cart_list = cart_list.split('#')
    carts = Cart.objects.filter(id__in=cart_list)
    for cart_obj in carts:
        print(cart_obj)
        cart_obj.c_is_select = not cart_obj.c_is_select  # 改变状态
        cart_obj.save()
    data = {
        'status': 200,
        'msg': 'ok',
        'totalprice': get_total_price(request.user)
    }
    return JsonResponse(data=data)


# 购物车商品的单选按钮
def changecartstate(request):
    cartid = request.GET.get('cartid')
    cart = Cart.objects.get(pk=cartid)
    cart.c_is_select = not cart.c_is_select  # 点击单选按钮则改变状态
    cart.save()
    is_all_select = not Cart.objects.filter(c_user_id=request.user).filter(
        c_is_select=False).exists()  # 如果存在未选中的商品，则全选更新为未选中
    data = {
        'status': 200,
        'msg': 'ok',
        'select': cart.c_is_select,
        'is_all_select': is_all_select,
        'totalprice': get_total_price(request.user)
    }
    return JsonResponse(data=data)


# 下单生成订单
def makeorder(request):
    carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)
    order = Order()
    order.o_user = request.user
    order.o_price = get_total_price(request.user)
    order.save()
    for cart in carts:
        ordergoods = OrderGoods()
        ordergoods.o_order_id = order.id
        ordergoods.o_goods_id = cart.c_goods_id
        ordergoods.o_goods_num = cart.c_goods_num
        ordergoods.save()
        cart.delete()  # 生成订单后删除购物车数据
    data = {
        'status': 200,
        'msg': 'ok',
        'orderid': order.id
    }
    return JsonResponse(data=data)


# 订单详情页面
def orderdetail(request):
    orderid = request.GET.get('orderid')
    order = Order.objects.get(pk=orderid)
    data = {
        'title': '订单详情',
        'order': order
    }
    return render(request, 'order/orderdetail.html', context=data)


# 全部订单列表
def allorderlist(request):
    orders = Order.objects.filter(o_user=request.user)
    data = {
        'title': '订单列表',
        'orders': orders
    }
    return render(request, 'order/orderlist.html', context=data)


# 未支付订单列表
def orderlistnotpay(request):
    orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NO_PAY)
    data = {
        'title': '订单列表',
        'orders': orders
    }
    return render(request, 'order/orderlist.html', context=data)


# 未收货订单列表
def orderlistnotreceive(request):
    orders = Order.objects.filter(o_user=request.user).filter(
        o_status__in=[ORDER_STATUS_NO_RECEIVE, ORDER_STATUS_NO_SEND])
    data = {
        'title': '订单列表',
        'orders': orders
    }
    return render(request, 'order/orderlist.html', context=data)


# 确认收货
def received(request):
    orderid = request.GET.get('orderid')
    order = Order.objects.get(pk=orderid)
    order.o_status = ORDER_STATUS_NO_COMMENT  # 修改订单状态由未收货到到确认收货
    order.save()
    data = {
        'status': 200,
        'msg': '确认收货成功'
    }
    return JsonResponse(data=data)


# 支付订单
def payed(request):
    orderid = request.GET.get('orderid')
    print(orderid)
    order = Order.objects.get(pk=orderid)
    order.o_status = ORDER_STATUS_NO_SEND  # 修改订单状态由未付款到已付款未发货
    order.save()
    data = {
        'status': 200,
        'msg': '支付成功'
    }
    return JsonResponse(data=data)


def logout(request):
    token = request.GET.get('token')
    cache.delete(token)  # 清缓存
    return render(request, 'user/login.html')


##收货地址页面
def addresslist(request):
    address = Address.objects.filter(a_user=request.user)
    data = {
        'status': 200,
        'address': address
    }
    return render(request, 'user/addresslist.html', context=data)


@csrf_exempt
def address(request):
    if request.method == 'GET':
        adrid = request.GET.get('id')
        if adrid:
            address = Address.objects.get(pk=adrid)
            data = {
                'address': address
            }
            return render(request, 'user/editaddress.html', context=data)
        else:
            return render(request, 'user/addaddress.html')
    if request.method == 'POST':
        a_name = request.POST.get('username')
        a_phone = request.POST.get('phone')
        a_address = request.POST.get('address')
        adrid = request.POST.get('adrid')
        token = request.POST.get('token')
        user = cache.get(token)
        if adrid:
            address = Address.objects.get(pk=adrid)
            address.a_name = a_name
            address.a_phone = a_phone
            address.a_address = a_address
        else:
            address = Address()
            address.a_name = a_name
            address.a_phone = a_phone
            address.a_address = a_address
            address.a_user_id = user
        address.save()
        data = {
            'status': 200,
            'msg': '保存成功'
        }
        return JsonResponse(data=data)
