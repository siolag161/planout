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
<<<<<<< HEAD
class EventCreateForm(forms.Form):
	
    name = forms.CharField()
=======
class EventCreateForm(forms.ModelForm):
	
    name = forms.CharField(
	    
    )
>>>>>>> 678fbc60f0063e903f814ee87edee882027f0f1e

    start_time = forms.DateTimeField( required=True,
    				      widget=DateTimeWidget(options={'format': 'dd/mm/yyyy hh:ii'} ))
    end_time = forms.DateTimeField( required=True,
    				    widget=DateTimeWidget(options={'format': 'dd/mm/yyyy hh:ii'} ))
<<<<<<< HEAD

    location = forms.CharField(required=True)

    location_place_name = forms.Field(required=False)
    location_address = forms.CharField(required=False)
    location_district = forms.CharField(required=False)
    
    location_city = forms.CharField(required=False)
    
    location_state = forms.Field(required=False)
    location_province = forms.Field(required=False)
    
    location_country = forms.CharField(required=False)
    
    location_longitude = forms.Field(required=False)
    location_latitude = forms.Field(required=False)
    location_place_id = forms.Field(required=False)
    location_url = forms.Field(required=False)
    location_website = forms.CharField(required=False)
    location_formatted_address = forms.Field(required=False)

    logo = forms.ImageField(required=False, )    

    description = forms.CharField(required=False, widget=forms.Textarea())
=======
    logo = forms.ImageField(required=False, )

    description = forms.CharField(required=False, widget=forms.Textarea())
    url = forms.URLField(required=False, )
>>>>>>> 678fbc60f0063e903f814ee87edee882027f0f1e
    is_online = forms.BooleanField(required=False, )
    category = forms.ChoiceField(choices = Event.EVENT_CATEGORY, initial = Event.EVENT_CATEGORY.performance, )

    topic = forms.ChoiceField(choices = Event.EVENT_TOPIC, initial = Event.EVENT_TOPIC.business, )
<<<<<<< HEAD
        
    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)

	self.helper = self._form_helper()
    
    class Meta:
	model = Event
	fields = ['name', 'start_time', 'end_time', 'location',  'logo', 'description',
		   'is_online', 'topic', 'category',]

=======
    
    #location = GeoJSONFormField(geom_type="Point", widget=forms.TextInput(), required=False, )

    
    class Meta:
	model = Event
	fields = ['name', 'start_time', 'end_time', 'logo', 'description',
		  'url', 'is_online', 'topic', 'category', 'location', ]
    
    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)

	self.helper = self._form_helper()
>>>>>>> 678fbc60f0063e903f814ee87edee882027f0f1e

    def get_success_url(self):
        return  "/"

    def _form_helper(self):
	helper = FormHelper()
	helper.form_show_labels = True
<<<<<<< HEAD
	# helper.form_class = 'form-horizontal'
	# helper.label_class = 'col-lg-3'
	# helper.field_class = 'col-lg-8'
	
        helper.layout = Layout(
	    Field('name', css_class=''),
	    Field('start_time', css_class=''),
	    Field('end_time', css_class=''),
	    Field('location', css_class='superlocation'),
	    Div(
		Div(
		    Div( Field('location_place_name',  data_geo='name'), css_class="toggle-field hidden"),
		    Div( Field('location_address' , data_geo='street_number'), css_class="toggle-field hidden"),	
		    Div( Field('location_district', data_geo='sublocality'), css_class="toggle-field hidden"),	
		    Div( Field('location_city',  data_geo='locality'), css_class="toggle-field hidden"),
		    # Div( Field('location_province' , data_geo='administrative_area_level_2'),
		    # 	 css_class="toggle-field hidden"),
		    
		    css_class = 'superlocation col-xs-6',	    
		),
		Div(
		    Div(
			css_class = 'map_canvas',    			
		    ),
		    css_id = "google_map_canvas_wrapper",
		    css_class = 'col-xs-6 toggle-field hidden',    

		),
		css_class = 'row fluid',	    		
	    ),
	    Div(		
	    Field('location_country',  data_geo='country', type="hidden"),		
		Field('location_place_id', data_geo='place_id', type="hidden"),
		Field('location_url',  data_geo='url', type="hidden"), 
		Field('location_website', data_geo='website', type="hidden"),
		Field('location_formatted_address', data_geo='formatted_address', type="hidden"),
		Field('location_latitude',  data_geo='lat', type="hidden", css_class="toggle-field hidden"),
		Field('location_longitude', data_geo='lng', type="hidden", css_class="toggle-field hidden"),
		Field('description', rows="3", css_class='input-xlarge'),
		css_class = 'superlocation',	    
	    ),	

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
=======
	#helper['peso'].wrap(AppendedText, "kg")
	helper.add_input(Submit('submit', 'Submit'))
        # helper.layout = Layout(
	#     Div(FormActions(
        #         Submit('submit', 'Sign Me Up', css_class = 'btn btn-pink full-width')
        #     ), css_class='input-group center-block'),
        # )
>>>>>>> 678fbc60f0063e903f814ee87edee882027f0f1e
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

