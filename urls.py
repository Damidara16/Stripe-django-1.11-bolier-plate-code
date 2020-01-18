from django.conf.urls import url
from . import views

app_name = 'banking'

urlpatterns = [
    url(r'^connect/$', views.connectCreation, name='preConnect'),
    url(r'^conf/$', views.confConnect, name='confConnect'),
    url(r'^precard/$', views.precard, name='precard'),
    url(r'^card-modify/$', views.modifyCard, name='modifyCard'),
]
