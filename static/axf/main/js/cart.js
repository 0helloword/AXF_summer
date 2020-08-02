$(function () {
    //增加商品数量
    var $addShopping=$(".addShopping");
    $addShopping.click(function () {
        console.log('add');
        $addShopping=$(this);
        token=window.localStorage.getItem("token");
        var goodsid=$addShopping.attr("goodsid");
        $.get('/app/addtocart/',{'goodsid':goodsid,'token':token},function (data) {
            console.log(data);
            if (data['status']===601){
                window.open('/app/login/',target="_self")
            }
            else if (data['status']===200){
                $('#total_price').html(data['total_price']);
                $addShopping.prev('span').html(data['good_num']);
            }
        })
    });

    //减少商品数量
    var $subShopping=$(".subShopping");
    $subShopping.click(function () {
        console.log('sub');
        $subShopping=$(this);
        var $li=$subShopping.parents("li");
        token=window.localStorage.getItem('token');
        var goodsid=$subShopping.attr("goodsid");
        $.get('/app/subtocart/',{'goodsid':goodsid,'token':token},function (data) {
            console.log(data);
            if (data['status']===601){
                window.open('/app/login/',target='_self')
            }
            else if(data['status']===200){
                $('#total_price').html(data['total_price']);
                if (data['good_num']>0){
                    $subShopping.next('span').html(data['good_num'])
                    }
                else {
                $li.remove();//购物车商品数量为0时，删除这条数据
                }
        }})
    });

    //全选功能--点一次点击，全选，第二次点击，全部取消选择
    var $allselect=$(".allselect");
    token=window.localStorage.getItem('token');
    $allselect.click(function () {
        console.log("all select");
        var select_list=[];
        var unselect_list=[];
        $(".confirm").each(function () {//循环获取商品是否被勾选的信息
            var $confirm = $(this);
            var cartid = $confirm.parents("li").attr("cartid");
            if ($confirm.find('span').find('span').html().trim()) {//如果span标签中不为空，则表示该商品已被勾选
                select_list.push(cartid);
            } else {//反之表明该商品未被勾选
                unselect_list.push(cartid);
            }
        });
        //如果未勾选的列表长度大于0，点击全选后，需要将所有的商品都勾选
        if (unselect_list.length>0){
            $.getJSON('/app/allselect/',{'cart_list':unselect_list.join('#'),'token':token},function (data) {//这里支持传字符串，不能传列表，所以使用join将id变成字符串，并用#分割
                console.log(unselect_list);
                if (data['status']===601){//用户未登陆则跳到登陆页面
                window.open('/app/login/',target="_self")
                }
                else if (data['status']===200){
                    $(".confirm").find('span').find('span').html('√');
                    $allselect.find('span').find('span').html('√');
                    $('#total_price').html(data['totalprice']);
                }
            })
            }
        //如果全部为勾选状态，点击全选后，将所有的商品都取消勾选,勾选控件置空
        else if(select_list.length>0){
            $.getJSON('/app/allselect/',{'cart_list':select_list.join('#'),'token':token},function (data) {
                console.log(data);
                if (data['status']===601){//用户未登陆则跳到登陆页面
                    window.open('/app/login/',target="_self")
                }
                else if (data['status']===200){
                    $(".confirm").find('span').find('span').html('');
                    $allselect.find('span').find('span').html('');
                    $('#total_price').html(data['totalprice']);
                }
            })
        }
        });

    //单选功能
    //单个商品的单选，点击选中，再点击取消选择
    //全选按钮的联动，全部商品都勾选时，全选按钮选中；只要有一个商品取消选择，全选按钮取消选择
    var $confirm=$(".confirm");
    $confirm.click(function () {
        var $confirm=$(this);
        token=window.localStorage.getItem('token');
        var $li=$confirm.parents('li');
        var cartid=$li.attr('cartid');//通过父标签li找到cartid
        var $allselect=$('.allselect');
        $.get('/app/changecartstate/',{'cartid':cartid,'token':token},function (data) {
            console.log(data);
            if (data['status']===601){//用户未登陆则跳到登陆页面
                window.open('/app/login/',target="_self")
            }
            if (data['status']===200){
                 $('#total_price').html(data['totalprice']);
                 if (data['select']){//改变商品的单选状态
                     $confirm.find('span').find('span').html('√');
                 }
                 else{
                     $confirm.find('span').find('span').html('');
                 }
                 if (data['is_all_select']){//改变全选按钮的状态
                     $allselect.find('span').find('span').html('√');
                 }
                 else{
                     $allselect.find('span').find('span').html('');
                 }
            }
        })
    });

    //生成订单
    var $make_order=$('#make_order');
    $make_order.click(function () {
        token = window.localStorage.getItem('token');
        var select_list = [];
        var unselect_list = [];
        $(".confirm").each(function () {
            var $confirm = $(this);
            var cartid = $confirm.parents('li').attr('cartid');
            if ($confirm.find('span').find('span').html().trim()) {
                select_list.push(cartid)
            } else {
                unselect_list.push(cartid)
            }
            if (select_list.length === 0) {
                return  //未勾选任何商品时点击无反应
            }
            $.get('/app/makeorder/', {'token': token}, function (data) {
                console.log(data);
                if (data['status'] === 601) {
                    window.open('/app/login/', target = '_self')
                } else if (data['status'] === 200) {//跳转到订单详情-支付页面
                    window.open('/app/orderdetail/?orderid='+data['orderid'], target = '_self')
                }
            })
        })
    })
    });

