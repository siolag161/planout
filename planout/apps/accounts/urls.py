# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from accounts import views

urlpatterns = patterns('',
    # URL pattern for the UserListView  # noqa
    url(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'
    ),
    # URL pattern for the UserRedirectView
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    # URL pattern for the UserDetailView
    url(
        regex=r'^(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    # URL pattern for the UserUpdateView
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
)
