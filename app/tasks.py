# 实现异步发送邮件，使用django中自带的发送邮件方法send_mail

from celery import shared_task
from django.core.mail import send_mail
from django.template import loader
from AXF.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT

@shared_task
def send_email(email, username, token):
    subject = "%s Activy" % username
    from_email = EMAIL_HOST_USER
    recipient_list = [email, ]
    data = {
        'username': username,
        'active_url': 'http://{}:{}/app/active/?u_token={}'.format(SERVER_HOST, SERVER_PORT, token)
    }
    html_message = loader.get_template('user/active.html').render(data)
    send_mail(subject=subject, message="", html_message=html_message, from_email=from_email,
              recipient_list=recipient_list, )
