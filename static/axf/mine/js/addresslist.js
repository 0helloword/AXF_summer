// 实现新增编辑收货地址
$(function () {
    //add只使用1次，所以可以用id定位
   $('#add').click(function () {
        token=localStorage.getItem('token');
        window.open('/app/address/?token='+token,target='_self')
    });

//编辑收货地址
    //id一个页面只可以使用一次；class可以多次引用。所以在循环列表中定位方法选择class
    $('.edit').click(function () {
        var $edit=$(this);
        var adrid=$edit.attr("adrid");
        console.log(adrid);
        window.open('/app/address/?id='+adrid,target='_self');

    })
});