from django.conf import settings

from appconf import AppConf
#from django.apps import AppConf
import datetime

class EventSettings(AppConf):
    # A "strftime" string for formatting start and end time selectors in forms
    TIMESLOT_TIME_FORMAT = '%I:%M %p'

    # Used for creating start and end time form selectors as well as time slot grids.
    # Value should be datetime.timedelta value representing the incremental 
    # differences between temporal options
    TIMESLOT_INTERVAL = datetime.timedelta(minutes=15)
    
    # A datetime.time value indicting the starting time for time slot grids and form
    # selectors
    TIMESLOT_START_TIME = datetime.time(9)
    
    # A datetime.timedelta value indicating the offset value from 
    # TIMESLOT_START_TIME for creating time slot grids and form selectors. The for
    # using a time delta is that it possible to span dates. For instance, one could
    # have a starting time of 3pm (15:00) and wish to indicate a ending value 
    # 1:30am (01:30), in which case a value of datetime.timedelta(hours=10.5) 
    # could be specified to indicate that the 1:30 represents the following date's
    # time and not the current date.
    TIMESLOT_END_TIME_DURATION = datetime.timedelta(hours=+8)
    
    # Indicates a minimum value for the number grid columns to be shown in the time
    # slot table.
    TIMESLOT_MIN_COLUMNS = 4
    
    # Indicate the default length in time for a new occurrence, specifed by using
    # a datetime.timedelta object
    DEFAULT_OCCURRENCE_DURATION = datetime.timedelta(hours=+2)
    
    # If not None, passed to the calendar module's setfirstweekday function.
    CALENDAR_FIRST_WEEKDAY = 6
        
    #
    AGE_RANGES = [ 0,1,5,10,15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100, 130] 
    #

    class Meta:
	prefix = 'event'


# settings_config = getattr(settings, 'EVENT_SETTINGS', {})

# for key, value in settings_config.items():
#     if key in EventSettings.__dict__:
#         setattr(AvatarConf, key, value)
#     else:
#         raise KeyError('Incorect option name of AVATAR in settings.py ({})'.format(key))
