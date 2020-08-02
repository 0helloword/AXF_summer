from django.core.mail import send_mail
from django.template import loader
from AXF.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT
from app.models import Cart


def send_email(email, username, token):
    subject = "%s Activy" % username
    from_email = EMAIL_HOST_USER
    recipient_list = [email, ]
    data = {
        'username': username,
        'active_url': 'http://{}:{}/app/active/?u_token={}'.format(SERVER_HOST, SERVER_PORT, token)#点击激活链接时则调用active方法
    }
    html_message = loader.get_template('user/active.html').render(data)
    send_mail(subject=subject, message="", html_message=html_message, from_email=from_email,
              recipient_list=recipient_list, )

def get_total_price(user):
    carts=Cart.objects.filter(c_is_select=True).filter(c_user=user)
    total=0
    for cart in carts:
        total+=cart.c_goods_num*cart.c_goods.price
    return "{:.2f}".format(total)
