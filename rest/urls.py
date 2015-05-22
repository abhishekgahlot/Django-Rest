from django.conf.urls import patterns, url
from rest import views

"""
Url's Required

user/signup
user/login
user/logout
user/{id} (to get and update user data)
user/ (save user data)
"""

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^login', views.rest_login, name='login'),
	url(r'^signup', views.rest_signup, name='signup'),
	url(r'^(\d+)/$', views.rest_user_details, name='user'),
	url(r'^logout', views.rest_logout, name='logout'),
	)