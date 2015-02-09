# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, InlineCheckboxes, FormActions

from allauth.account.forms import LoginForm, SignupForm

from .models import BasicUser

class UserForm(forms.ModelForm):
    class Meta:
        # Set this form to use the User model.
        model = BasicUser
        # Constrain the UserForm to just these fields.
        fields = ("first_name", "last_name")

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



