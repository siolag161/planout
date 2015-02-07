
import allauth.account.app_settings as app_settings
from allauth.utils import get_form_class
from allauth.account.forms import LoginForm as DefaultLoginForm, SignupForm as DefaultSignupForm

def account(request):
    # We used to have this due to the now removed
    # settings.CONTACT_EMAIL. Let's see if we need a context processor
    # in the future, otherwise, deprecate this context processor
    # completely.
    return { 'login_form': get_form_class( app_settings.FORMS, 'login', DefaultLoginForm),
	     'signup_form': get_form_class( app_settings.FORMS, 'signup', DefaultSignupForm)  }
