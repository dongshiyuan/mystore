#coding=utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#用户信息
class User(AbstractUser):
    qq = models.CharField(max_length=11, blank=True, null=True, verbose_name="QQ号码")
    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name="手机号")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ["-id"]

    def __str__(self):
        return self.username


#广告
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name="标题")
    image_url = models.ImageField(upload_to="ad/%Y/%m/%d", verbose_name="图片路径")
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    index = models.IntegerField(default=1, verbose_name="排列顺序")

    class Meta:
        verbose_name = "广告"
        verbose_name_plural = verbose_name
        ordering = ["index","id"]

    def __str__(self):
        return self.title


#分类
class Category(models.Model):
    type = models.CharField(max_length=50, verbose_name="标题")
    sex = models.CharField(choices=(("m","男"),("w","女")), max_length=2, default="m", verbose_name="性别")
    name = models.CharField(max_length=50, verbose_name="分类名称")
    index = models.IntegerField(default=1, verbose_name="排列顺序")

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name
        ordering = ["index", "id"]

    def __str__(self):
        return self.name


#品牌
class Brand(models.Model):
    name = models.CharField(max_length=20, verbose_name="品牌名称")
    index = models.CharField(default=1, max_length=10, verbose_name="排列顺序")

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name
        ordering = ["index",]

    def __str__(self):
        return self.name

#尺寸
class Size(models.Model):
    name = models.CharField(max_length=20, verbose_name="尺寸")
    index = models.CharField(default=1, max_length=10, verbose_name="排列顺序")

    class Meta:
        verbose_name = "尺寸"
        verbose_name_plural = verbose_name
        ordering = ["index",]

    def __str__(self):
        return self.name


#标签
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name="标签")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


#商品信息
class Clothing(models.Model):
    category = models.ForeignKey(Category, verbose_name="分类")
    name = models.CharField(max_length=30, verbose_name="名称")
    brand = models.ForeignKey(Brand, verbose_name="品牌")
    size = models.ManyToManyField(Size, verbose_name="尺寸")
    old_price = models.FloatField(default=0.0, verbose_name="原价")
    new_price = models.FloatField(default=0.0, verbose_name="现在")
    discount = models.FloatField(default=1.0, verbose_name="折扣")
    desc = models.CharField(max_length=100, verbose_name="简介")
    sales = models.IntegerField(default=0, verbose_name="销量")
    tag = models.ForeignKey(Tag, verbose_name="标签")
    inventory_num = models.IntegerField(default=0, verbose_name="库存")
    image_url_i = models.ImageField(upload_to="clothing/%Y/%m/%d", default="clothing/default.jpg",
                                    verbose_name="展示图片路径")
    image_url_l = models.ImageField(upload_to="clothing/%Y/%m/%d", default="clothing/default.jpg",
                                    verbose_name="详情图片路径1")
    image_url_m = models.ImageField(upload_to="clothing/%Y/%m/%d", default="clothing/default.jpg",
                                    verbose_name="详情图片路径2")
    image_url_r = models.ImageField(upload_to="clothing/%Y/%m/%d", default="clothing/default.jpg",
                                    verbose_name="详情图片路径3")
    image_url_c = models.ImageField(upload_to="clothing/%Y/%m/%d", default="clothing/default.jpg",
                                    verbose_name="购物车展示图片")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name
        ordering = ["id",]

    def __str__(self):
        return self.brand.name + "---" + self.category.name


#购物车
class Caritem(models.Model):
    clothing = models.ForeignKey(Clothing, verbose_name="购物车中的商品")
    quantity = models.IntegerField(default=0, verbose_name="数量")
    sum_price = models.FloatField(default=0.0, verbose_name="小计")

    class Meta:
        verbose_name = "购物车条目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


#购物车
class Cart(object):
    def __init__(self):
        self.items = []
        self.total_price = 0.0

    def add(self, clothing):
        self.total_price += clothing.new_price

        for item in self.items:
            if item.clothing.id == clothing.id:
                item.quantity += 1
                item.sum_price += clothing.new_price
                break
        else:
            self.items.append(Caritem(clothing=clothing, quantity=1, sum_price=clothing.new_price))
