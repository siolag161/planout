import base64

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    def get_user_model():
        return User
    custom_user_model = False
else:
    custom_user_model = True
    
#==========================================================================
def base64_normalize(encoded_url):
    paddings = (4 - len(encoded_url)%4)
    encoded_url += "=" * paddings
    return encoded_url

#==========================================================================
def base64_decode_url(encoded_url):
    encoded_url = base64_normalize(encoded_url)
    return base64.urlsafe_b64decode(encoded_url)

#==========================================================================
def url_safe_normalize(encoded_url):
    encoded_url = encoded_url.replace("=","")
    return encoded_url
    
#==========================================================================
def base64_encode_url(string):
    encoded_url = base64.urlsafe_b64encode(string)
    return url_safe_normalize(encoded_url)

#==========================================================================
def get_user(username):
    """ Return user from a username/ish identifier """
    if custom_user_model:
        return get_user_model().objects.get_by_natural_key(username)
    else:
        return get_user_model().objects.get(username=username)
