# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

import views
urlpatterns = patterns('',
    # URL pattern for the UserListView  # noqa
		       
    url(
        regex=r'^~create$',
        view=views.EventCreateView.as_view(),
        name='event_create_form'
    ),
)
