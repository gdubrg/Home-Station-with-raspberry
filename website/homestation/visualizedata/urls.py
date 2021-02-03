from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('visualizesettings', views.settings),
    # re_path(r'^insert/(?P<sensor>[a-z]+)/(?P<value>[0-9]+)$', views.insertvalues),
    re_path(r'^insert/(?P<sensor>[a-z0-9]+)/(?P<value>[0-9]+)$', views.insertvalues.as_view()),
    re_path(r'^insert/(?P<sensor>[a-z0-9]+)$', views.insertSensor.as_view()),
    path('sensors', views.sensors),
    path('sensors_live', views.sensors_live),
    re_path(r'^dynamic/(?P<data_type>[a-z0-9_]+)$', views.DynamicData.as_view()),
]
