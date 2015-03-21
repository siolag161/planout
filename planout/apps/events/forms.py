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

from tinymce.widgets import TinyMCE
from core.widgets.datetime_widgets import SplitDateTimeWidget


#=======================================================================
class EventCreateForm(forms.ModelForm):
	
    name = forms.CharField()


    start_time = forms.SplitDateTimeField( input_date_formats=['%d/%m/%Y'],
					   input_time_formats=['%I:%M%p'],
					   required=True,
					   widget=SplitDateTimeWidget())
    end_time = forms.SplitDateTimeField( input_date_formats=['%d/%m/%Y'],
					   input_time_formats=['%I:%M%p'],
					   required=True,
					   widget=SplitDateTimeWidget())

    location = forms.CharField(required=True)

    avenue_name = forms.Field(required=False)

    place_name = forms.Field(required=False)
    route = forms.CharField(required=False)
    street_number = forms.CharField(required=False)

    district = forms.CharField(required=False)

    city = forms.CharField(required=False)    
    # province = forms.Field(required=False)
    state = forms.Field(required=False)    
    country_code = forms.CharField(required=False)

    longitude = forms.Field(required=False)
    latitude = forms.Field(required=False)
    place_id = forms.Field(required=False)
    website_url = forms.Field(required=False)
    formatted_address = forms.Field(required=False)

    logo = forms.ImageField(required=False, )    

    description = forms.CharField(required=False,
				  widget=TinyMCE(attrs={ 'rows': 30, 'cols': 167}))
    
    is_online = forms.BooleanField(required=False, )
        
    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)
	self.helper = self._form_helper()
    
    class Meta:
	model = Event
	fields = ['name', 'start_time', 'end_time', 'logo', 'description', "avenue_name",
		   'is_online',]


    def get_success_url(self):
        return  "/"

    def _form_helper(self):
	helper = FormHelper()
	helper.form_show_labels = True    
	
        helper.layout = Layout(
	    Field('name', css_class=''),
	    Div(
		Div( Field('start_time'), css_class = 'start-time-wrapper col-xs-6',),
		Div( Field('end_time'),    css_class = 'end-time-wrapper col-xs-6', ),		
		css_class = 'row fluid',	    		
	    ),
	    Field('location', css_class='superlocation'),
	    Div( 
		Div(		    
		    Div( Field('avenue_name',  data_geo='name'), css_class="toggle-field hid"),

		    Div(			
			Div( Field('street_number' , data_geo='street_number'), css_class="toggle-field hid col-xs-6"),
			Div( Field('route' , data_geo='route'), css_class="toggle-field hid col-xs-6"),
			css_class = 'row fluid',	    		

		    ),
		    Div( Field('district', data_geo='locality'), css_class="toggle-field hid"),	
		    Div( Field('city',  data_geo='administrative_area_level_1'), css_class="toggle-field hid"),
		    # Div( Field('province', data_geo='state'), css_class="toggle-field hid"),

		    Div( HTML('<a href="#" class="location-reset pull-right">Reset location</a>'), css_class="toggle-field hid"),
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
		Field('state' , data_geo='state', type="hidden"),
		Field('place_name',  data_geo='name', type="hidden"),
		Field('country_code',  data_geo='country_short', type="hidden",),
		Field('place_id', data_geo='place_id', type="hidden",),
		Field('website_url',  data_geo='website', type="hidden",), 
		Field('formatted_address', data_geo='vicinity', type="hidden",),
		Field('latitude',  data_geo='lat', type="hidden",),
		Field('longitude', data_geo='lng', type="hidden",),
		css_class = 'superlocation',	    
	    ),	
	    Field('description', rows="3", css_class='input-xlarge'),

	    Field('logo', css_class=''),
	    Field('is_online', css_class=''),
	 )
	helper.add_input(Submit('submit', 'Submit'))
	return helper
