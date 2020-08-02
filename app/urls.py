from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^market/$', views.market, name='market'),
    url(r'^marketwithparams/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/', views.marketwithparams, name='marketwithparams'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^register/',views.register,name='register'),
    url(r'^login/$',views.login,name='login'),
    url(r'^checkuser/',views.checkuser,name='checkuser'),#验证用户名是否重复
    url(r'^checkemail/',views.checkemail,name='checkemail'),
    url(r'^checkpassword/',views.checkpassword,name='checkpassword'),
    url(r'^logout/',views.logout,name='logout'),
    url(r'^active/',views.active,name='active'),
    # url(r'^sendemail/',views.send_email,name='send_email'),
    url(r'^addtocart/',views.addtocart,name='addtocart'),
    url(r'^subtocart/',views.subtocart,name='subtocart'),
    url(r'^changecartstate/',views.changecartstate,name='changecartstate'),
    url(r'^allselect/',views.allselect,name='allselect'),
    url(r'^makeorder/',views.makeorder,name='makeorder'),
    url(r'orderdetail/',views.orderdetail,name='orderdetail'),
    url(r'allorderlist/',views.allorderlist,name='orderlist'),
    url(r'orderlistnotpay/',views.orderlistnotpay,name='orderlistnotpay'),
    url(r'orderlistnotreceive/',views.orderlistnotreceive,name='orderlistnotreceive'),
    url(r'payed/',views.payed,name='payed'),
    url(r'received/',views.received,name='received'),
    url(r'^addresslist/$',views.addresslist,name='address'),
    url(r'^address/$',views.address,name='editaddress'),
    # url(r'alipay/',views.alipay,name='alipay'),
]
