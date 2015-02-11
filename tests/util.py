
from django.core.urlresolvers import reverse

def get_login_redirect_url(target_url):
    return '%s?next=%s' % (reverse('account_login'), target_url)
