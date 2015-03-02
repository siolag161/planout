# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, InlineCheckboxes, FormActions

#from .models import BasicUser
from .models import Event
# from leaflet.forms.fields import PointField
# from leaflet.forms.widgets import LeafletWidge
from django.utils.timezone import now
from datetime import datetime, timedelta
from functools import partial


from core.widgets import DateTimeWidget


#=======================================================================
class EventCreateForm(forms.ModelForm):
	
    name = forms.CharField(
	    
    )

    start_time = forms.DateTimeField( required=True,
    				      widget=DateTimeWidget(options={'format': 'dd/mm/yyyy hh:ii'} ))
    end_time = forms.DateTimeField( required=True,
    				    widget=DateTimeWidget(options={'format': 'dd/mm/yyyy hh:ii'} ))
    logo = forms.ImageField(required=False, )

    description = forms.CharField(required=False, widget=forms.Textarea())
    url = forms.URLField(required=False, )
    is_online = forms.BooleanField(required=False, )
    category = forms.ChoiceField(choices = Event.EVENT_CATEGORY, initial = Event.EVENT_CATEGORY.performance, )

    topic = forms.ChoiceField(choices = Event.EVENT_TOPIC, initial = Event.EVENT_TOPIC.business, )
    
    #location = GeoJSONFormField(geom_type="Point", widget=forms.TextInput(), required=False, )

    
    class Meta:
	model = Event
	fields = ['name', 'start_time', 'end_time', 'logo', 'description',
		  'url', 'is_online', 'topic', 'category', 'location', ]
    
    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)

	self.helper = self._form_helper()

    def get_success_url(self):
        return  "/"

    def _form_helper(self):
	helper = FormHelper()
	helper.form_show_labels = True
	#helper['peso'].wrap(AppendedText, "kg")
	helper.add_input(Submit('submit', 'Submit'))
        # helper.layout = Layout(
	#     Div(FormActions(
        #         Submit('submit', 'Sign Me Up', css_class = 'btn btn-pink full-width')
        #     ), css_class='input-group center-block'),
        # )
	return helper


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

