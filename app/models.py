from django.db import models

from app.views_constant import ORDER_STATUS_NO_PAY


class Main(models.Model):
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    trackid = models.IntegerField(default=1)

    class Meta:
        abstract = True


class MainWheel(Main):
    # axf_wheel(img, name, trackid)
    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    # axf_nav(img,name,trackid)
    class Meta:
        db_table = 'axf_nav'


class MainMustbuy(Main):
    # axf_mustbuy(img,name,trackid)
    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(Main):
    # axf_shop(img,name,trackid)
    class Meta:
        db_table = 'axf_shop'


class MainShow(Main):
    # axf_mainshow(trackid, name, img, categoryid, brandname, img1, childcid1, productid1, longname1, price1,
    #              marketprice1, img2, childcid2, productid2, longname2, price2, marketprice2, img3, childcid3,
    #              productid3, longname3, price3, marketprice3)
    categoryid = models.IntegerField(default=1)
    brandname = models.CharField(max_length=50)
    img1 = models.CharField(max_length=255)
    childcid1 = models.IntegerField(default=1)
    productid1 = models.IntegerField(default=1)
    longname1 = models.CharField(max_length=128)
    price1 = models.FloatField(default=0.0)
    marketprice1 = models.FloatField(default=0.0)
    img2 = models.CharField(max_length=255)
    childcid2 = models.IntegerField(default=1)
    productid2 = models.IntegerField(default=1)
    longname2 = models.CharField(max_length=128)
    price2 = models.FloatField(default=0.0)
    marketprice2 = models.FloatField(default=0.0)
    img3 = models.CharField(max_length=255)
    childcid3 = models.IntegerField(default=1)
    productid3 = models.IntegerField(default=1)
    longname3 = models.CharField(max_length=128)
    price3 = models.FloatField(default=0.0)
    marketprice3 = models.FloatField(default=0.0)

    class Meta:
        db_table = 'axf_mainshow'


class FoodType(models.Model):
    # axf_foodtypes(typeid, typename, childtypenames, typesort)
    typeid = models.IntegerField(default=1)
    typename = models.CharField(max_length=50)
    childtypenames = models.CharField(max_length=255)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtype'


class Goods(models.Model):
# axf_goods(productid,productimg,productname,productlongname,isxf,pmdesc,specifics,price,
# marketprice,categoryid,childcid,childcidname,dealerid,storenums,productnum)
    productid=models.IntegerField(default=1)
    productimg=models.CharField(max_length=255)
    productname=models.CharField(max_length=50)
    productlongname=models.CharField(max_length=255)
    isxf=models.BooleanField(default=False)
    pmdesc=models.BooleanField(default=False)
    specifics=models.CharField(max_length=255)
    price=models.FloatField(default=0.0)
    marketprice=models.FloatField(default=0.0)
    categoryid=models.IntegerField(default=1)
    childcid=models.IntegerField(default=1)
    childcidname=models.CharField(max_length=255)
    dealerid=models.IntegerField(default=1)
    storenums=models.IntegerField(default=1)
    productnum=models.IntegerField(default=1)
    class Meta:
        db_table='axf_goods'

class AXFUser(models.Model):
    u_username=models.CharField(max_length=32,unique=True)
    u_password=models.CharField(max_length=256)
    u_email=models.CharField(max_length=64,unique=True)
    u_icon=models.ImageField(upload_to='icon/%Y/%m/%d/')#将图片按照年月日的文件夹管理
    is_active=models.BooleanField(default=False)
    is_delete=models.BooleanField(default=False)
    class Meta:
        db_table='axf_user'

class Cart(models.Model):
    c_user=models.ForeignKey(AXFUser)
    c_goods=models.ForeignKey(Goods)
    c_goods_num=models.IntegerField(default=1)
    c_is_select=models.BooleanField(default=True)
    class Meta:
        db_table='axf_cart'

class Order(models.Model):
    o_user=models.ForeignKey(AXFUser)
    o_price=models.FloatField(default=0)
    o_time=models.DateTimeField(auto_now=True)
    o_status=models.IntegerField(default=ORDER_STATUS_NO_PAY)
    class Meta:
        db_table='axf_order'

class OrderGoods(models.Model):
    o_order=models.ForeignKey(Order)
    o_goods=models.ForeignKey(Goods)
    o_goods_num=models.IntegerField(default=1)
    class Meta:
        db_table='axf_ordergoods'

class Address(models.Model):
    a_name=models.CharField(max_length=64,default='summer')
    a_address=models.CharField(max_length=128)
    a_phone=models.CharField(max_length=32,default=123)
    a_user=models.ForeignKey(AXFUser)
    class Meta:
        db_table='axf_address'