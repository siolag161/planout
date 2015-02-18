# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, InlineCheckboxes, FormActions

#from .models import BasicUser
from .models import Event
from djgeojson.fields import GeoJSONFormField
# from leaflet.forms.fields import PointField
# from leaflet.forms.widgets import LeafletWidget

#=======================================================================
class EventForm(forms.Form):

    name = forms.CharField(
	
    )

    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()

    logo = forms.ImageField()

    description = forms.CharField(widget=forms.Textarea())
    url = forms.URLField()
    is_online = forms.BooleanField()
    category = forms.ChoiceField(choices = Event.EVENT_CATEGORY)
    topic = forms.ChoiceField(choices = Event.EVENT_TOPIC)
    
    location = GeoJSONFormField(geom_type="Point", widget=forms.TextInput())
    
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
	

        # self.helper = self._form_helper()

    def _form_helper(self):
	helper = FormHelper()
	helper.form_show_labels = False
        helper.layout = Layout(
	    
        )
	return helper


	#         fields = ( "name", "start_time", "end_time", "location", "logo",
# 		   "description", "url", "is_online", "topic", "category")

#=======================================================================
# class EventForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super(EventForm, self).__init__(*args, **kwargs)
	
# 	helper = FormHelper()
# 	#helper.form_show_labels = False
#         # helper.layout = Layout(
# 	#     AppendedText('email', '<i class="glyphicon glyphicon-user"></i>'),
# 	#     AppendedText('password1', '<i class="glyphicon glyphicon-lock"></i>',
#         #                   placeholder='Password', autocomplete='off',
#         #                   widget=forms.PasswordInput, css_class="form-control"),
# 	#     AppendedText('password2', '<i class="glyphicon glyphicon-lock"></i>',
# 	# 		 placeholder='Confirm Password', autocomplete='off',
# 	# 		 widget=forms.PasswordInput, css_class="form-control"),
#         #     Div(FormActions(
#         #         Submit('submit', 'Sign Me Up', css_class = 'btn btn-pink full-width')
#         #     ), css_class='input-group center-block'),
#         # )
#         # self.helper = helper
    
#     class Meta:
#         # Set this form to use the User model.
#         model = Event
#         # Constrain the Form to just these fields.
#         fields = ( "name", "start_time", "end_time", "location", "logo",
# 		   "description", "url", "is_online", "topic", "category")

