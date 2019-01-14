from django.conf.urls import url
from . import views
urlpatterns=[
    url('^login/$',views.login,name='login'),
    url(r'^upload/$',views.upload,name='upload'),
    url(r'^lists/$',views.lists,name='lists'),
    url(r'^download/$',views.download),
    url(r'^delete/$',views.delete),
    url(r'^logout/$',views.logout),
]
