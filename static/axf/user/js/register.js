$(function () {
    //判断用户名是否可用
    var $username = $("#username_input");
    $username.change(function () {
        var username = $username.val().trim();//获取用户名并且去掉头尾空格
        if (username.length) {
            //将用户名发送给服务器进行预校验
            $.getJSON('/app/checkuser/', {'username': username}, function (data) {
                console.log(data);
                $username_info = $("#username_info");
                if (data['status'] === 200) {
                    $username_info.html("用户名可用").css('color', 'green')
                } else if (data['status'] === 901) {
                    $username_info.html("用户名已存在").css('color', 'red')
                }
            })
        }
    });

    //判断邮箱是否可用
    var $email = $("#email_input");
    $email.change(function () {
        var email = $email.val().trim();
        if (email.length) {
            //将邮箱发送给服务器进行预校验
            $.getJSON('/app/checkemail/', {'email': email}, function (data) {
                console.log(data);
                var $email_info = $("#email_info");
                if (data['status'] === 200) {
                    $email_info.html('邮箱可用').css('color', 'green')
                } else if (data['status'] === 901) {
                    $email_info.html('邮箱已存在').css('color', 'red')
                }
            })
        }
    });


    //判断两次密码是否一致
    var $password = $('#password_input');
    var $password_confirm = $('#password_confirm_input');
    $password_confirm.change(function () {
        var password = $password.val().trim();
        var password_confirm = $password_confirm.val().trim();
        if (password_confirm.length) {
            $.getJSON('/app/checkpassword/', {
                'password': password,
                'password_confirm': password_confirm
            }, function (data) {
                var $password_info = $('#password_info');
                console.log(data);
                if (data['status'] === 200) {
                    $password_info.html('两次密码输入一致').css('color', 'green')
                } else if (data['status'] === 801) {
                    $password_info.html('两次密码不一致').css('color', 'red')
                }
            })
        }

    })
});

//配合register.html元素form中的onsubmit="return check()"使用
function check() {
    //用户名不能为空
    var $username = $('#username_input');
    var username = $username.val().trim();
    if (!username) {
        var $username_info = $("#username_info");
        $username_info.html('用户名不能为空').css('color', 'red');
        return false;
    }
    //邮箱不能为空
    var $email = $('#email_input');
    var email = $email.val().trim();
    if (!email) {
        var $email_info = $("#email_info");
        $email_info.html('邮箱不能为空').css('color', 'red');
        return false;
    }

    //密码和确认密码不能为空
    var $password = $('#password_input');
    var $password_confirm = $('#password_confirm_input');
    password = $password.val().trim();
    password_confirm = $password_confirm.val().trim();
    var $password_info = $("#password_info");
    if (!password_confirm || !password) {
        $password_info.html('密码不能为空').css('color', 'red');
        return false;
    }

    //用户名，邮箱，密码任意一个元素有红色提示时均不可注册
    var info_color1 = $("#username_info").css('color');
    var info_color2 = $("#email_info").css('color');
    var info_color3 = $('#password_info').css('color');
    console.log(info_color1,info_color2,info_color3);
    if (info_color1 == 'rgb(255, 0, 0)' || info_color2 == 'rgb(255, 0, 0)'|| info_color3=='rgb(255, 0, 0)' ) {//颜色这里中间一定要加空格
        return false
    }
    //注册时将前端的密码进行md5加密展示
    var $password_input=$("#password_input");
    var password=$password_input.val().trim();
    $password_input.val(md5(password));
    var $password_confirm_input=$("#password_confirm_input");
    var password_confirm=$password_confirm_input.val().trim();
    $password_confirm_input.val(md5(password_confirm));
    return true
}

