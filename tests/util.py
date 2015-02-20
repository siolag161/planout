
from django.core.urlresolvers import reverse
import urllib
def get_login_redirect_url(target_url):
    return '%s?next=%s' % (reverse('account_login'), urllib.quote(target_url))
