$(function () {
    var $username = $("#username_input");
    var $password = $("#password_input");
    var $login = $("#login");
    var $login_info = $('#login_info');
    $login.click(function () {
        var username = $username.val().trim();
        var password = $password.val().trim();
        console.log(username, password);
        if (!username || !password) {
            $login_info.html('用户名或密码不能为空').css('color', 'red');
        } else {
            $password.val(md5(password));
            //将用户名发送给服务器进行预校验
            $.post('/app/login/', {'username': username, 'password': md5(password)}, function (data) {
                console.log(data);
                if (data['status'] === 200) {
                    const token = data.token;//将登陆接口返回的token设置为一个变量token
                    window.localStorage.setItem('token', token);//将token本地保存以便后面需要登陆的接口使用
                    window.open("/app/home/", target = "_self");
                } else if (data['status'] === 701) {
                    $login_info.html('用户名或密码错误').css('color', 'red');
                }
            })
        }
    })
});


//校验用户名或密码为空时返回提示信息
function parse_data() {
    var $username_input = $('#username_input');
    var $password_input = $('#password_input');
    var $login_info = $('#login_info');
    var username = $username_input.val().trim();
    var password = $password_input.val().trim();
    console.log(username, password);
    if (!username || !password) {
        $login_info.html('用户名或密码不能为空').css('color', 'red');
        return false;
    }
    //有红色提示时均不可登陆
    var info_color = $("#login_info").css('color');
    console.log(info_color);
    if (info_color == 'rgb(255, 0, 0)') {//颜色这里中间一定要加空格
        return false
    }
    return true
}

