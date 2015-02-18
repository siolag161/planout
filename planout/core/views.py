from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from django.http import (HttpResponseRedirect, Http404,
                         HttpResponsePermanentRedirect)

#==========================================================================================
class HomeView(TemplateView):
    template_name = 'pages/home.html'

home = cache_page(60 * 10)(HomeView.as_view())

#==========================================================================================
import logging
logger = logging.getLogger('werkzeug')

#==========================================================================================
def _ajax_response(request, response, adapter, form=None):
    if request.is_ajax():
        if (isinstance(response, HttpResponseRedirect)
                or isinstance(response, HttpResponsePermanentRedirect)):
            redirect_to = response['Location']
        else:
            redirect_to = None
        response = adapter.ajax_response( request,
					  response,
					  form=form,
					  redirect_to=redirect_to)
    return response
    
#==========================================================================================
class RedirectAuthenticatedMixin(object):
    def dispatch(self, request, *args, **kwargs):
        # WORKAROUND: https://code.djangoproject.com/ticket/19316
        self.request = request
        # (end WORKAROUND)
        if request.user.is_authenticated():
            redirect_to = self.get_authenticated_redirect_url()
            response = HttpResponseRedirect(redirect_to)
            return response
        else:
            response = super(RedirectAuthenticatedMixin,
                             self).dispatch(request,
                                            *args,
                                            **kwargs)
        return response

    def get_authenticated_redirect_url(self):
        redirect_field_name = self.redirect_field_name
        return get_login_redirect_url(self.request,
                                      url=self.get_success_url(),
                                      redirect_field_name=redirect_field_name)
	
#==========================================================================================   
class AjaxableFormViewMixin(object):
    def get_adapter(self):
	raise NotImplementedError("Implement the adapter please (%s)"
				    % self.__class__.__name__.lower())
    
    def post(self, request, *args, **kwargs):	
	adapter = self.get_adapter()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            response = self.form_valid(form)
        else:  
            response = self.form_invalid(form)
        return _ajax_response(self.request, response, adapter, form=form)
