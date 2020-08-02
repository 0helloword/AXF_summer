$(function () {
    //订单详情页面支付结果的跳转
    //判断未登陆则跳转到登陆页面，登陆且付款成功跳转到个人中心页面
    $alipay = $('#alipay');
    $alipay.click(function () {
        token = window.localStorage.getItem('token');
        var orderid = $alipay.attr('orderid');
        $.get('/app/payed/', {'orderid': orderid, 'token': token}, function (data) {
            console.log(data);
            if (data['status'] === 601) {
                window.open('/app/login/', target = '_self')
            } else if (data['status'] === 200) {
                window.open('/app/mine/?token=' + token, target = '_self')
            }
        })
    });
//订单详情页面确认收货结果的跳转
//判断未登陆则跳转到登陆页面，登陆且收货成功跳转到个人中心页面
    var $receive = $('#receive');
    orderid = $receive.attr('orderid');
    token = window.localStorage.getItem('token');
    $receive.click(function () {
        $.get('/app/received/', {'orderid': orderid, 'token': token}, function (data) {
            if (data['status'] === 601) {
                window.open('/app/login/', target = '_self')
            } else if (data['status'] === 200) {
                window.open('/app/mine/?token=' + token, target = '_self')
            }
        })
    })
})
