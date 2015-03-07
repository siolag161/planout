from django import forms
from .conf import EventSettings as config

#=======================================================================
import logging
logger = logging.getLogger('werkzeug')
class AgeRangeWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None) :
	min_val_attrs, max_val_attrs = None, None
	if attrs:
	    min_val_class = attrs['min_class']
	    max_val_class = attrs['max_class']
	    del attrs['min_val_class']
	    del attrs['max_val_class']

	    max_val_attrs = attrs.copy()
	    max_val_attrs['class'] = max_val_class
	    min_val_attrs = attrs.copy()
	    min_val_attrs['class'] = min_val_class            
        
        widgets = ( forms.Select(attrs=min_val_attrs, choices=[(age,age) for age in config.AGE_RANGES] ),
		    forms.Select(attrs=max_val_attrs, choices=[(age,age) for age in config.AGE_RANGES])  )
        
        super(AgeRangeWidget, self).__init__(widgets, attrs)
    
    def decompress(self, value):
        if value:
	    min_val, max_val = [int(v) for v in value.split("-")]
            # min_val, max_val = (value[0], value[1])
            # max_val = strftime("%I", value.timetuple())
            # minute = strftime("%M", value.timetuple())
            # meridian = strftime("%p", value.timetuple())
	    logger.info("value: %s" % value)
            return (min_val, max_val)
        else:
            return (None,None)

    # class Media:
