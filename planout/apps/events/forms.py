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
class EventCreateForm(forms.Form):
	
    name = forms.CharField()

    start_time = forms.DateTimeField( required=True,
    				      widget=DateTimeWidget(options={'format': 'dd/mm/yyyy hh:ii'} ))
    end_time = forms.DateTimeField( required=True,
    				    widget=DateTimeWidget(options={'format': 'dd/mm/yyyy hh:ii'} ))

    location = forms.CharField(required=True)

    location_place_name = forms.Field(required=False)
    location_address_1 = forms.Field(required=False)
    location_address_2 = forms.Field(required=False)
    location_city = forms.Field(required=False)
    location_state = forms.Field(required=False)
    location_province = forms.Field(required=False)
    location_country = forms.CharField(required=False)
    
    logo = forms.ImageField(required=False, )    

    description = forms.CharField(required=False, widget=forms.Textarea())
    is_online = forms.BooleanField(required=False, )
    category = forms.ChoiceField(choices = Event.EVENT_CATEGORY, initial = Event.EVENT_CATEGORY.performance, )

    topic = forms.ChoiceField(choices = Event.EVENT_TOPIC, initial = Event.EVENT_TOPIC.business, )
        
    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)

	self.helper = self._form_helper()
    
    class Meta:
	model = Event
	fields = ['name', 'start_time', 'end_time', 'location',  'logo', 'description',
		   'is_online', 'topic', 'category',]


    def get_success_url(self):
        return  "/"

    def _form_helper(self):
	helper = FormHelper()
	helper.form_show_labels = True
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-lg-3'
	helper.field_class = 'col-lg-8'

        helper.layout = Layout(

	    Field('name', css_class=''),
	    Field('start_time', css_class=''),
	    Field('end_time', css_class=''),
	    Div( 
		Field('location', css_class=''),
		Field('location_place_name', type='hidden', data_geo='street_number', css_class=""),
		Field('location_address_1' , type='hidden', css_class=""),
		Field('location_address_2', type='hidden', css_class=""),
		Field('location_city', type='hidden', css_class=""),
		Field('location_state', type='hidden', css_class=""),
		Field('location_province' , type='hidden', css_class=""),
		Field('location_country' , type='hidden', css_class=""),
		
		css_id = 'superlocation',
	    ),
	    Field('description', rows="3", css_class='input-xlarge'),

	    Field('logo', css_class=''),
	    # # Field('url', css_class=''),
	    Field('is_online', css_class=''),
	    # Field('topic', css_class=''),
	    # Field('category', css_class=''),

	    #  FormActions(
	    #  	Submit('save_changes', 'Save changes', css_class="btn-primary"),
	    # # 	Submit('cancel', 'Cancel', css_class=""),
	    # # 	css_class="submit_group"
	    #  )
	 )
	# helper.add_input(Submit('submit', 'Submit'))
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

