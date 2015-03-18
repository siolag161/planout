from datetime import datetime
import re
import uuid

from django.forms import forms, widgets
from django.forms.widgets import MultiWidget, DateTimeInput, DateInput, TimeInput
from django.utils.formats import get_format, get_language
from django.utils.safestring import mark_safe
from django.utils.six import string_types

try:
    from django.forms.widgets import to_current_timezone
except ImportError:
    to_current_timezone = lambda obj: obj # passthrough, no tz support

BOOTSTRAP_INPUT_TEMPLATE =   """
       <div id="inner_div_%(id)s" class="input-group %(fieldtype)s">
           %(rendered_widget)s
           %(clear_button)s
           <span class="input-group-addon"><span class="glyphicon %(glyphicon)s"></span></span>
       </div>
    """
      

CLEAR_BTN_TEMPLATE = """<span class="input-group-addon">
  <span class="glyphicon glyphicon-remove"></span>
</span>"""




#=======================================================================
import logging
logger = logging.getLogger('werkzeug')
class PickerWidgetMixin(object):
    format_name = None
    glyphicon = None
    fieldtype = "date"
    def __init__(self, attrs=None,):
        if attrs is None:
            attrs = {'readonly': ''}

        self.is_localized = False
        self.format = None
        super(PickerWidgetMixin, self).__init__(attrs, format=self.format)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        rendered_widget = super(PickerWidgetMixin, self).render(name, value, final_attrs)
        #if not set, autoclose have to be true.
        # Use provided id or generate hex to avoid collisions in document
        id = final_attrs.get('id', uuid.uuid4().hex)
	clearBtn = True
        return mark_safe(
            BOOTSTRAP_INPUT_TEMPLATE % dict(
		id=id,
		rendered_widget=rendered_widget,
		clear_button=CLEAR_BTN_TEMPLATE if clearBtn else "",
		glyphicon=self.glyphicon,
		fieldtype=self.fieldtype
	    )
        )


class DateTimeWidget(PickerWidgetMixin, DateTimeInput):
    fieldtype = "datetime"

    """
    DateTimeWidget is the corresponding widget for Datetime field, it renders both the date and time
    sections of the datetime picker.
    """

    format_name = 'DATETIME_INPUT_FORMATS'
    glyphicon = 'glyphicon-th'

    def __init__(self, attrs=None):


        super(DateTimeWidget, self).__init__(attrs)


class DateWidget(PickerWidgetMixin, DateInput):
    """
    DateWidget is the corresponding widget for Date field, it renders only the date section of
    datetime picker.
    """

    format_name = 'DATE_INPUT_FORMATS'
    glyphicon = 'glyphicon-calendar'
    fieldtype = "date"

    def __init__(self, attrs=None, date_options=None, ):
        super(DateWidget, self).__init__(attrs)


class TimeWidget(PickerWidgetMixin, TimeInput):
    """
    TimeWidget is the corresponding widget for Time field, it renders only the time section of
    datetime picker.
    """

    format_name = 'TIME_INPUT_FORMATS'
    glyphicon = 'glyphicon-time'
    fieldtype = "time"

    def __init__(self, attrs=None, time_options=None, ):
        super(TimeWidget, self).__init__(attrs)

###############================================================================

SPLIT_DATETIME_TEMPLATE = """
       <div class="split_datetime">
         <div class="date_input_wrapper col-xs-6">
           %(rendered_date)s
         </div>
         <div class="time_input_wrapper col-xs-6">
           %(rendered_time)s 
         </div>
       </div>
"""
class SplitDateTimeWidget(MultiWidget):
    def __init__(self, attrs=None, options=None, date_options=None,
		 time_options=None, usel10n=None):
	if date_options: date_options = dict(options, **date_options)
        if time_options: time_options = dict(options, **time_options)

        widgets = (DateWidget(attrs=attrs, date_options=date_options,),
                   TimeWidget(attrs=attrs, time_options=time_options,))
        super(SplitDateTimeWidget, self).__init__(widgets, attrs=attrs)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]	    

    def format_output(self, rendered_widgets):
	return mark_safe(
	    SPLIT_DATETIME_TEMPLATE % dict(
		rendered_date =  rendered_widgets[0],
		rendered_time = rendered_widgets[1]
	    )
	)

          
