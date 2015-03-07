# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.forms.extras.widgets import SelectDateWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Div, Submit, HTML, Button,
				 Row, Field, ButtonHolder, MultiWidgetField)
from crispy_forms.bootstrap import AppendedText, InlineCheckboxes, FormActions
from django.template.defaultfilters import filesizeformat # for avatar upload

from allauth.account.forms import LoginForm, SignupForm
from .models import BasicUser
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import datetime
from .conf import settings

#============== User Edit Form #===============================
class UserEditForm(forms.ModelForm):
    """

    """
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    birthdate = forms.DateField( widget=SelectDateWidget(
	years=range(1910, datetime.date.today().year)),
    )   
    description = forms.CharField(required=False,
        widget = forms.Textarea(),
    )
    phone_number = PhoneNumberField(label="Phone", required=False,widget=PhoneNumberPrefixWidget(initial='VN',
		       attrs={'prefix_class':'phone_prefix', 'phone_class':'phone_number'}),)
    
    def __init__(self, *args, **kwargs):
	super(UserEditForm, self).__init__(*args, **kwargs)
	helper = FormHelper(self)
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-lg-2'
	helper.field_class = 'col-lg-8'
	

        helper.layout = Layout(
	    Field('first_name', css_class=''),
	    Field('last_name', css_class=''),
	    MultiWidgetField('birthdate'),
	    Field('description', css_class=''),
	    MultiWidgetField('phone_number'),	    
	    FormActions(
		Submit('save_changes', 'Save changes', css_class="btn-primary"),
		Submit('cancel', 'Cancel', css_class=""),
		css_class="submit_group"
	    )
	 )
	self.helper = helper

    

    class Meta:
        model = BasicUser
        fields = ("first_name", "last_name", "birthdate", "description", "phone_number")

### SIGNUP FORM

class UserSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
	
	self.fields['password1'].widget = forms.PasswordInput()
	self.fields['password2'].widget = forms.PasswordInput()
	
	helper = FormHelper()
	helper.form_show_labels = False
        helper.layout = Layout(
	    AppendedText('email', '<i class="glyphicon glyphicon-user"></i>'),
	    AppendedText('password1', '<i class="glyphicon glyphicon-lock"></i>',
                          placeholder='Password', autocomplete='off',
                          widget=forms.PasswordInput, css_class="form-control"),
	    AppendedText('password2', '<i class="glyphicon glyphicon-lock"></i>',
			 placeholder='Confirm Password', autocomplete='off',
			 widget=forms.PasswordInput, css_class="form-control"),
            Div(FormActions(
                Submit('submit', 'Sign Me Up', css_class = 'btn btn-pink full-width')
            ), css_class='input-group center-block'),
        )
        self.helper = helper
    
### END SIGNUP FORM
    
class UserLoginForm(LoginForm):    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
	
	self.fields['password'].widget = forms.PasswordInput()
	helper = FormHelper()
	self.fields['login'].label = False
	self.fields['password'].label = False
        helper.layout = Layout(
	    AppendedText('login', '<i class="glyphicon glyphicon-user"></i>'),
	    AppendedText('password', '<i class="glyphicon glyphicon-lock"></i>',
                          placeholder='Password', autocomplete='off',
                          widget=forms.PasswordInput, css_class="form-control"),
	    Div(Field('remember', label = 'Remember Me', css_class="remember_me_field"),
		HTML('<a href="%s">Forgot password?</a>' % (reverse('account_reset_password'))), css_class="remember-forgot-wrapper clearfix"),
            Div(FormActions(
                Submit('submit', 'Log Me In', css_class = 'btn btn-pink full-width')
            ), css_class='input-group center-block'),
        )
        self.helper = helper

'''
'''
class UserLogoutForm(forms.ModelForm):
    pass

#===================================================

class UserAvatarUploadForm(forms.Form):
    avatar = forms.ImageField(label=("Avatar"))
    avatar_src = forms.Field(required=False)
    avatar_data = forms.Field(required=False)

    def __init__(self, *args, **kwargs):
        #self.user = kwargs.pop('user')
	super(UserAvatarUploadForm, self).__init__(*args, **kwargs)
 
	helper = FormHelper()
	helper.form_action = reverse('profiles:avatar_add')
	helper.form_show_labels = False
	helper.layout = Layout(
	    Div(
		# Field('avatar_src', type="hidden", css_class="avatar-src"),
		Field('avatar_data', type="hidden", css_class="avatar-data", required=False),
		HTML('<div class="btn btn-default btn-upload-file"><span>Upload your avatar</span>'),
		Field('avatar', id='avatarInput', css_class="avatar-input", required=False),
		HTML('</div>'),
		css_class="avatar-upload",
	    ),
	)
        self.helper = helper

    def clean_avatar(self):
        data = self.cleaned_data['avatar']
	if data.size > settings.PROFILE_AVATAR_MAX_SIZE:
	    error = _("Your file is too big (%(size)s), "
		      "the maximum allowed size is %(max_valid_size)s")

	    raise forms.ValidationError(error % {
		 'size': filesizeformat(data.size),
		'max_valid_size': filesizeformat(settings.PROFILE_AVATAR_MAX_SIZE)
	    })
	if settings.PROFILE_AVATAR_ALLOWED_FILE_EXTS:
            root, ext = os.path.splitext(data.name.lower())
            if ext not in settings.PROFILE_AVATAR_ALLOWED_FILE_EXTS:
                valid_exts = ", ".join(settings.PROFILE_AVATAR_ALLOWED_FILE_EXTS)
                error = _("%(ext)s is an invalid file extension. "
                          "Authorized extensions are : %(valid_exts_list)s")
                raise forms.ValidationError(error %
                                            {'ext': ext,
                                             'valid_exts_list': valid_exts})
        # return


