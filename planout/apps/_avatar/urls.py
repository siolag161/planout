try:
    from django.conf.urls import patterns, url
except ImportError:
    # Django < 1.4
    from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('avatar.views',
    url(r'^add/$', 'add', name='avatar_add'),
)
