# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse
from django.forms import ModelForm
# view imports
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import ListView

# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin


# Import the form from users/forms.py
from .forms import UserForm

# Import the customized User model
from .models import BasicUser, base64_decode_url, base64_normalize


class UserDetailView(LoginRequiredMixin, DetailView):
    model = BasicUser
    # # These next two lines tell the view to index lookups by username
    slug_field = "encoded_email"
    slug_url_kwarg = "encoded_email"    
    template_name = 'accounts/user_detail.html' 

      
    # def get_object(self):
    #     # Only get the User record for the user making the request
    # 	# encoded_email = base64_normalize()
    #     # return BasicUser.objects.get( encoded_email = decoded_email )
    # 	return BasicUser.objects.get(encoded_email=self.request.user.encoded_email)

    
class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False
	
    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    form_class = UserForm

    # we already imported User in the view code above, remember?
    model = BasicUser

    template_name = 'accounts/user_form.html' 

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"encoded_email": self.request.user.encoded_email})

    def get_object(self):
        # Only get the User record for the user making the request
        return BasicUser.objects.get(encoded_email=self.request.user.encoded_email)


class UserListView(LoginRequiredMixin, ListView):
    model = BasicUser
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


###### BEGIN AVATAR
# class AvatarChangeForm(ModelForm):
#     class Meta:
#         model = BasicUser
#         fields = ['avatar']

# def change_avatar(request):
#     if request.method == 'POST':
#         form = AvatarChangeForm(request.POST, request.FILES,
#                                 instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/profile/')
#     else:
#         form = AvatarChangeForm(instance=request.user.profile)

#     return render(request, 'template.html', {'form': form})
###### 
