from django.conf.urls import url

from . import views # import view.py in urls.py

app_name = 'ecomapps'

urlpatterns = [
    url(r'^$', views.listing, name="listing"), #"ecomapps/void
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'^search/$', views.search, name="search")
]