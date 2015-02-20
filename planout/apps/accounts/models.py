# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import IntegrityError

from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.mail import send_mail


from django_extensions.db.fields import ShortUUIDField  # give the UUID field @todo -> once move to 1.8 use the native PostgreSQL

from avatar.fields import AvatarField

# Import the basic Django ORM models library
from django.db import models

from django.utils.translation import ugettext_lazy as _

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

# Subclass AbstractUser
# todo: enforce uniqueness
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
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    avatar = AvatarField(max_length=1024, blank=True) 

    objects = BasicUserManager()
    USERNAME_FIELD = 'email'	# 

    def set_email(self, email):
	self.email = email


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
	    return self.email

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

    
    def __unicode__(self):
	if self.username != '':
	    return self.username
	else:
	    return self.email
