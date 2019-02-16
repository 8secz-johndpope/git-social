from django.conf.urls import url
from django.contrib import admin
from . import api

urlpatterns = [
    url(r'^api/v1/(?P<owner>\w+)/(?P<repo>\w+)/user/(?P<username>\w+)/lines/week/?$', api.get_lines_week, name="get_lines_week"),
    url(r'^api/v1/(?P<owner>\w+)/(?P<repo>\w+)/user/(?P<username>\w+)/commits/week/?$', api.get_commits_week, name="get_lines_week"),
    url(r'^api/v1/(?P<owner>\w+)/(?P<repo>\w+)/leaderboard/commits/week/?$', api.get_leaderboard_commits_week, name="get_commits_week"),
]
