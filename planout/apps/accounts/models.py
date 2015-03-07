# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import IntegrityError

from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.mail import send_mail

from django.db import models
import core.models as core_models
from core.fields import BaseImageField, AutoCreatedField, AutoLastModifiedField

from django_extensions.db.fields import ShortUUIDField  # give the UUID field @todo -> once move to 1.8 use the native PostgreSQL

from .fields import AvatarField
from phonenumber_field.modelfields import PhoneNumberField

# Import the basic Django ORM models library
from django.db import models

from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from .util import ( get_primary_avatar, get_default_avatar_url,
                          get_avatar_url_or_defaul_url)

user_model_label = getattr(settings, "AUTH_USER_MODEL", "auth.User")

class BasicUserManager(BaseUserManager):
    def create_user(self, email, password):
	if not email:
	    raise ValueError('Users must have an email')
	email = self.normalize_email(email)
	user = self.model()
	user.is_active = True
	user.set_password(password)
	user.email = email # user.set_email(email)
	self.save_automatic_unique_username(user, email)
	return user

    def create_superuser(self, email, password):
        user = self.create_user(email = email, password=password)
        user.is_staff = True
        user.is_superuser = True
	# user.set_email(email)
	self.save_automatic_unique_username(user, email)
        return user

    def save_automatic_unique_username(self, user, email):
	try:
	    user.username = self.generate_username_from_email(email)	    
	    user.save(using=self._db)
	except IntegrityError: # unique constraint violation
	    user.save(using=self._db)
	    user.username = self.generate_username_from_email(email, user.id)	    
	    user.save(using=self._db)

    def generate_username_from_email(self, email, unique_id = ""):
	""" get """
	return "%s%s" % (email.split("@")[0], unique_id)

class BasicUser(AbstractBaseUser,PermissionsMixin):
    #redefine basic data fields
    username = models.CharField(_('username'), max_length=30, unique=True, null=True,
				help_text=_('Required. 30 characters or fewer. Letters, digits and '
					    '@/./+/-/_ only.'),
				validators=[
                                             RegexValidator(r'^[\w.@+-]+$',
							      _('Enter a valid username. '
								'This value may contain only letters, numbers '
								'and @/./+/-/_ characters.'), 'invalid'),
				],
        error_messages={
	    'unique': _("A user with that username already exists."),
	})
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True,  max_length=100, blank=True)
    
    uuid = ShortUUIDField(version=4)

    is_staff = models.BooleanField(_('staff status'), default=False,
				   help_text=_('Designates whether the user can log into this admin '
					       'site.'))
    is_active = models.BooleanField(_('active'), default=True,
				    help_text=_('Designates whether this user should be treated as '
						'active. Unselect this instead of deleting accounts.'))
    
    date_joined =  AutoCreatedField(_('date joined'), editable=False,)

    birthdate = models.DateField(null=True, blank=True)

    avatar = AvatarField(max_length=1024, blank=True) 

    description = models.TextField(help_text=_("Please enter the description"),
				   verbose_name=_("description"), blank=True, null=True)
    
    phone_number = PhoneNumberField(blank=True, null=True)

    modified = AutoLastModifiedField(_('modified'), editable=False,)
    # phone_number = 

    objects = BasicUserManager()
    USERNAME_FIELD = 'email'	# 

    def set_email(self, email):
	self.email = email

    @property
    def avatar_url(self):
	return get_avatar_url_or_defaul_url(self)
	
    @property
    def display_name(self):
	if self.first_name:
	    return self.first_name
	else:
	    return self.username	

    @property
    def full_name(self):
	return self.get_full_name()
	
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        if full_name.strip() != '':
	    return full_name.strip()
	else:
	    return self.display_name

    def get_short_name(self):
        "Returns the short name for the user."
	if self.first_name.strip() != '':
	    return self.first_name.strip()
	else:
	    return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


    def get_absolute_url(self):
	from django.core.urlresolvers import reverse
        return reverse("profiles:edit_profile_uuid", kwargs={'uuid': self.uuid})

    
    def __unicode__(self):
	if self.username != '':
	    return self.username
	else:
	    return self.email



#================================================================================
class ProfessionalProfile(core_models.BaseType):
    owner = models.ForeignKey(user_model_label, verbose_name=_("Owner"), related_name="pro_profiles")
    '''
    The organizer of the event
    '''    
    logo =  BaseImageField(blank=True, max_length=1024)

    '''
    contact fields
    '''
    email = models.EmailField(max_length=100, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    fax_number = PhoneNumberField(blank=True, null=True)

    @property
    def url_name(self):
	return "pro:detail"

    @property
    def source_from(self):
	return "name"
    
    def __unicode__(self):
	return self.name

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and (self.owner == other.owner and self.name == other.name))	    
