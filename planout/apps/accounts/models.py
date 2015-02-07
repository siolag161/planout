# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.mail import send_mail

from awesome_avatar.fields import AvatarField


# Import the basic Django ORM models library
from django.db import models

from django.utils.translation import ugettext_lazy as _

class BasicUserManager(BaseUserManager):
    def create_user(self, email, password):
	if not email:
	    raise ValueError('Users must have an email')
	user = self.model(email=self.normalize_email(email))
	user.is_active = True
	user.set_password(password)
	user.save(using=self._db)
	return user

    def create_superuser(self,  email, password):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



# Subclass AbstractUser
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
    is_staff = models.BooleanField(_('staff status'), default=False,
				   help_text=_('Designates whether the user can log into this admin '
					       'site.'))
    is_active = models.BooleanField(_('active'), default=True,
				    help_text=_('Designates whether this user should be treated as '
						'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    avatar = AvatarField(upload_to='avatars', width=100, height=100) 

    objects = BasicUserManager()
    USERNAME_FIELD = 'email'	# 

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        if self.full_name.strip() != '':
	    return self.full_name.strip()
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
