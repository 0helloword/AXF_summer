//实现编辑,新增地址，保存
$(function () {
    var $username = $("#username_input");
    var $phone = $("#phone_input");
    var $address = $("#address_input");
    var $save = $("#save");
    adrid=$save.attr('adrid');
    $save.click(function () {
        var username = $username.val().trim();
        var phone = $phone.val().trim();
        var address = $address.val().trim();
        console.log(username);
        token=localStorage.getItem('token');
        $.post('/app/address/', {'adrid':adrid,'username': username, 'phone': phone, 'address': address,'token':token}, function (data) {
            console.log(data);
            if (data['status']===200){
                window.open('/app/addresslist/?token='+token,target='_self')
            }
        })
    })
});



