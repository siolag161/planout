from django.apps import AppConfig


class ExtAllauthConfig(AppConfig):
    name = 'extensions.allauth'
    label = 'Allauth Extensions'

default_app_config = 'extensions.allauth.ExtAllauthConfig'
