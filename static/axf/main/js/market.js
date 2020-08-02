$(function () {
    $("#all_types").click(function () {
        console.log("全部类型");
        var $all_type_container=$("#all_type_container");
        $all_type_container.show();
        var $all_type=$(this);
        var $span=$all_type.find("span").find("span");
        $span.removeClass('glyphicon glyphicon-chevron-down').addClass('glyphicon glyphicon-chevron-up');//将向下箭头改为向上箭头
        var $sort_rule_container=$("#sort_rule_container");
        $sort_rule_container.slideUp();
        var $sort_rule=$("#sort_rule");
        var $span_sort_rule=$sort_rule.find("span").find("span");
        $span_sort_rule.removeClass('glyphicon glyphicon-chevron-up').addClass('glyphicon glyphicon-chevron-down')
    });
    
    $("#all_type_container").click(function () {
         var $all_type_container=$(this);
         $all_type_container.hide();
        var $all_type=$("#all_types");
        var $span=$all_type.find("span").find("span");
        $span.removeClass('glyphicon glyphicon-chevron-up').addClass('glyphicon glyphicon-chevron-down')
    });
    
     $("#sort_rule").click(function () {
        console.log("排序");
        var sort_rule_container=$("#sort_rule_container");
        sort_rule_container.slideDown();
        var sort_rule=$(this);
        var $span=sort_rule.find("span").find("span");
        $span.removeClass('glyphicon glyphicon-chevron-down').addClass('glyphicon glyphicon-chevron-up');
         var $all_types_container=$("#all_types_container");
        $all_types_container.hide();
        var $all_types=$("#all_types");
        var $span_all_type=$all_types.find("span").find("span");
        $span_all_type.removeClass('glyphicon glyphicon-chevron-up').addClass('glyphicon glyphicon-chevron-down')
    });

    $("#sort_rule_container").click(function () {
         var sort_rule_container=$(this);
         sort_rule_container.hide();
        var $all_type=$("#all_types");
        var $span=$all_type.find("span").find("span");
        $span.removeClass('glyphicon glyphicon-chevron-up').addClass('glyphicon glyphicon-chevron-down')
    })
});

$(".addShopping").click(function () {
    console.log("add");
    var $add=$(this);
    var goodsid=$add.attr("goodsid");
    var token = window.localStorage.getItem("token");//获取本地存储的token传到后台去校验
    $.get('/app/addtocart/',{'goodsid':goodsid,'token':token},function (data) {
        console.log(data);
        if (data['status']===601){//用户未登陆则跳到登陆页面
            window.open('/app/login/',target="_self")
        }
        else if (data['status']=== 200){
            $add.prev('span').html(data['good_num']);
        }
    })
});


$(".subShopping").click(function () {
    console.log('sub');
    var $sub=$(this);
    var goodsid=$sub.attr('goodsid');
    var token = window.localStorage.getItem("token");
    $.get('/app/subtocart/',{'goodsid':goodsid,'token':token},function (data) {
        console.log(data);
        if (data['status']===601){//用户未登陆则跳到登陆页面
            window.open('/app/login/',target="_self")
        }
        else if (data['status']===200){//减少商品
            $sub.next('span').html(data['good_num'])//获取到数字元素(subShopping的下一个元素)点击-则数字减1
        }
        else if (data['status']===204){//商品数量为0时减少商品弹窗提示
            alert('不能再少啦！');
        }
     })
});