from django.shortcuts import render, redirect
from django.views.generic import View
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.db.models import F
from pure_pagination import Paginator, PageNotAnInteger

from .forms import *
from .utils import authenticated_view,LoginRequiredMixin
from .models import *
# Create your views here.


def global_setting(request):
    #站点信息
    MEDIA_URL = settings.MEDIA_URL
    category_list = Category.objects.all()
    #男装分类信息
    category_list_m = [c for c in category_list if c.sex == 'm']
    #女装分类信息
    category_list_f = [c for c in category_list if c.sex == 'w']
    #品牌信息
    brand_list = Brand.objects.all()
    #热销榜
    hot_list = Clothing.objects.all().order_by("-sales")[:4]
    #标签
    tag_list = Tag.objects.all()
    #购物车
    cart = request.session.get(request.user.id, None)
    return locals()


class Index(View):
    def get(self, request):
        ad_list = Ad.objects.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        clo_list = Clothing.objects.all()

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(clo_list, request=request, per_page=8)

        clothing = p.page(page)

        return render(request, "index.html",locals())


#产品列表页
class Product(View):

    def get(self, request):
        sex = request.GET.get('sex','m')
        try:
            category = Category.objects.get(sex=sex)
        except Category.DoesNotExist:
            return render(request, 'error.html', {'reason': '分类不存在'})
        clo_list = Clothing.objects.filter(category=category)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(clo_list, request=request, per_page=8)
        clothing = p.page(page)
        return render(request, 'products.html', locals())



#标签列表页
class Tags(View):
    pass


#商品详情页
class Detail(View):
    def get(self, request):
        did = int(request.GET.get('did',''))
        try:
            clo = Clothing.objects.get(pk=did)
        except Clothing.DoesNotExist:
            return render(request, 'single.html', {"reason": "该商品不存在"})
        return render(request, 'single.html', locals())


#品牌列表页
class Brands(View):
    pass


#注册
class Register(View):
    def post(self,request):
        regform = RegForm(request.POST)
        if  regform.is_valid():
            user = User.objects.create(username=regform.cleaned_data["username"],
                                        email=regform.cleaned_data["email"],
                                        password=make_password(regform.cleaned_data["password"]))
            user.save()
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
            return redirect(request.POST.get("source_url"))
        else:
            return render(request,'error.html', {"reason": regform.errors})

    def get(self,request):
        regform = RegForm()
        return render(request, 'register.html', locals())


#登陆
class Login(View):

    def post(self, request):
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data["username"]
            password = loginform.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                user.backend = "django.contrib.auth.backends.ModelBackend"
                login(request, user)
                return redirect(request.POST.get("source_url",""))
            else:
                return render(request, 'error.html', {"reason": "登陆验证失败"})
        else:
            return render(request, 'error.html', {"reason": loginform.errors})

    def get(self, request):
        loginform = LoginForm()
        return render(request, 'login.html', locals())


#退出
class Logout(View):
    def get(self, request):
        logout(request)
        loginform = LoginForm()
        return render(request, 'login.html', locals())


#查看购物车
class View_cart(LoginRequiredMixin,View):
    def get(self, request):
        cart = request.session.get(request.user.id, None)
        return render(request, 'checkout.html', locals())



#添加购物车
class Add_cart(LoginRequiredMixin,View):

    def post(self, request):
        chid = int(request.POST.get('chid', None))
        try:
            clothing = Clothing.objects.get(id=chid)
        except Clothing.DoesNotExist:
            return render(request, 'error.html', {"reason": "商品不存在"})
        cart = request.session.get(request.user.id, None)
        if cart is None:
            cart = Cart()
            cart.add(clothing)
        else:
            cart.add(clothing)
        request.session[request.user.id] = cart
        return render(request, 'checkout.html', locals())


#清空购物车
class Clean_cart(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart()
        return render(request, 'checkout.html', locals())


#删除商品
class Clean_one_item(View):

    pass


#打折商品
class Discount_item(View):

    def get(self, request):
        clo_list = Clothing.objects.filter(new_price__lt=F('old_price'))
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(clo_list, request=request, per_page=8)
        clothing = p.page(page)
        return render(request, 'products.html', locals())












