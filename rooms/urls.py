from django.urls import re_path
from . import views

app_name = 'rooms'

urlpatterns = [
    re_path(r'^new/$', views.CreateRoom.as_view(), name='create'),
    re_path(r"^by/(?P<username>[-\w]+)/$", views.UserRooms.as_view(),name='roomlist'),
    re_path(r"^by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",views.RoomDetail.as_view(),name="single"),
    re_path(r"^delete/(?P<pk>\d+)/$",views.DeleteRoom.as_view(),name="delete"),
    re_path(r"^update/(?P<username>[-\w]+)/(?P<pk>\d+)/$", views.UpdateRoom.as_view(),name='update'),
]