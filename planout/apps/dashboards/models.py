# from django.db import models
# import core.models as core_models


# # Create your models here.

# class ProfessionalProfile(core_models.OwnedModel, core_models.BaseType):
#     '''
#     The organizer of the event
#     '''    
#     logo =  BaseImageField(blank=True, max_length=1024)

#     '''
#     contact fields
#     '''
#     email = models.EmailField(max_length=100, blank=True)
#     phone_number = PhoneNumberField(blank=True, null=True)
#     fax_number = PhoneNumberField(blank=True, null=True)

#     @property
#     def url_name(self):
# 	return "pro:detail"

#     @property
#     def source_from(self):
# 	return "name"
    
#     def __unicode__(self):
# 	return self.name
