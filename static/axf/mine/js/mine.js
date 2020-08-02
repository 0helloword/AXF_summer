// 个人中心页面跳转

$(function () {
    token=window.localStorage.getItem('token');
    //点击未登陆跳转到登陆页面
    $("#not_login").click(function () {
        window.open('/app/login/','_self')
    });
    //点击待付款跳转到待付款订单页面
    $("#not_pay").click(function () {
        window.open('/app/orderlistnotpay/?token='+token,target='_self')
    });
    //点击待收货跳转到待收货订单页面
    $("#not_receive").click(function () {
        window.open('/app/orderlistnotreceive/?token='+token,target='_self')
    });
    //点击全部订单跳转到全部订单页面
    $("#allorder").click(function () {
        window.open('/app/allorderlist/?token='+token,target='_self')
    });
    //点击收货地址跳转到地址列表页面
    var $address=$("#address");
    $address.click(function () {
        window.open('/app/addresslist/?token='+token,target='_self')
    });
    //点击退出跳转到登陆页面
    $("#logout").click(function () {
        window.open('/app/logout/?token='+token,target='_self')
    })
});