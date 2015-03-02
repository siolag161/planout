# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

import views

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
    url(
        #regex=r'^(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$',
#	regex=r'^(?P<encoded_email>[A-Za-z0-9-_]+)$',
	regex=r'^edit/(?P<uuid>[2-9A-HJ-NPQ-Za-km-z]{22})$',

        view=views.UserEditView.as_view(),
        name='edit_profile_uuid'
    ),
    # URL pattern for the UserUpdateView
    # url(
    #     regex=r'^~update/$',
    #     view=views.UserUpdateView.as_view(),
    #     name='update'
    # ),

    url(r'^avatar/add/$', views.AvatarAddView.as_view(), name='avatar_add'),
	
)
