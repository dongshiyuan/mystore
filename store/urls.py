from django.conf.urls import url, include

from .views import *

urlpatterns = [
    url(r"^$", Index.as_view(), name="index"),
    url(r'^products/$', Product.as_view(), name="products"),
    url(r'^tags/$', Tags.as_view(), name="tags"),
    url(r'^detail/$',Detail.as_view(), name="detail"),
    url(r'^register/$', Register.as_view(), name="register"),
    url(r'^login/$', Login.as_view(), name="login"),
    url(r'^logout/$', Logout.as_view(), name="logout"),
    url(r'^view_cart/$', View_cart.as_view(), name="view_cart"),
    url(r'^add_cart/$', Add_cart.as_view(), name="add_cart"),
    url(r'^clean_cart/$', Clean_cart.as_view(), name="clean_cart"),
    url(r'^brands/$', Brands.as_view(), name="brands"),
    url(r'^discount/$', Discount_item.as_view(), name="discount"),
]