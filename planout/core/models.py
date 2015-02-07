# Import the basic Django ORM models library
from django.db import models

from django.utils.translation import ugettext_lazy as _

class BaseType(models.Model):
    name = models.CharField(max_length=80, help_text=_("Please enter the name"), verbose_name=_("name"))
    alternative_name = models.CharField(max_length=80,
					help_text=_("Please enter the alternative name"),
					verbose_name=_("alternative name"))
    description = models.TextField(help_text=_("Please enter the description"),
					verbose_name=_("desciption"))
    url = URLField()

    
				   

