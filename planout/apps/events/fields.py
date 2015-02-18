
from django.db import models
from django import forms
from django.forms import fields
from django.utils.translation import ugettext_lazy as _
from .conf import EventSettings as config

#=======================================================================
import logging
logger = logging.getLogger('werkzeug')

from .widgets import AgeRangeWidget
class AgeRangeFormField(forms.fields.MultiValueField):
    widget = AgeRangeWidget
    #validators = []
    
    def __init__(self, *args, **kwargs):
	max_length = kwargs.pop('max_length')	
	all_fields = (
	    #forms.fields.ChoiceInput
	    fields.TypedChoiceField( label='Min Age', coerce=int, 
				     empty_value='0', initial = 0,choices=[(age,age) for age in config.AGE_RANGES] ),
	    fields.TypedChoiceField( label='Max Age', coerce=int, 
				     empty_value='70', initial = '70', choices=[(age,age) for age in config.AGE_RANGES] )
	)
	super(AgeRangeFormField, self).__init__(all_fields, *args, **kwargs)

    def compress(self, data_list):
        """
        Takes the values from the MultiWidget and passes them as a
        list to this function. This function needs to compress the
        list into a single object to save.
        """
        if data_list:
            if not (data_list[0] and data_list[1]):
                raise forms.ValidationError("Field is missing data.")
	    min_age, max_age = data_list[0], data_list[1]
	    if not ( min_age < max_age ):
		raise forms.ValidationError("Max Age must > Min Age")
	    result_string = "%d-%d" % (min_age,max_age)
	    return result_string
        return None
	
#=======================================================================
class AgeRangeField(models.CharField):    
    __metaclass__ = models.SubfieldBase
     
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', '0-130')
	kwargs.setdefault('max_length', '7')
	kwargs.setdefault('verbose_name', _('Age range'))
        super(AgeRangeField, self).__init__(*args, **kwargs)
	
    def deconstruct(self):
        name, path, args, kwargs = super(AgeRangeField, self).deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs
	
    def to_python(self, value):
	if not value:
	    return None
	elif isinstance(value, basestring):
	    return tuple(map(int, value.split('-')))
	elif not isinstance(value, (tuple, list)):
	    raise ValidationError('Unable to convert %s to value' % value)    
	return tuple(value)		

    def get_prep_value(self, value):
    	return "%s-%s" % (value[0], value[1])

    def value_to_string(self, instance):
	val = getattr(instance, self.name)
	if val:
	    return "%s-%s" % (value[0], value[1])
	return None

    def formfield(self, **kwargs):
        defaults = {'form_class': AgeRangeFormField}
        # defaults['width'] = self.width
        # defaults['height'] = self.height
        defaults.update(kwargs)
        return super(AgeRangeField, self).formfield(**defaults)

#=======================================================================
#=======================================================================
