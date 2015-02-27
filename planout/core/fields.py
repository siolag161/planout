from __future__ import unicode_literals
#from django.db.models import SubfieldBase
from django.utils import six
from django.db import models
from django.utils.timezone import now
import slugify
import copy

import os
import hashlib
#from django.utils import force_bytes
from django.utils.encoding import force_bytes

import logging

logger = logging.getLogger('werkzeug')
""" django-model-utils """
class Choices(object):
    """
    A class to encapsulate handy functionality for lists of choices
    for a Django model field.

    Each argument to ``Choices`` is a choice, represented as either a
    string, a two-tuple, or a three-tuple.

    If a single string is provided, that string is used as the
    database representation of the choice as well as the
    human-readable presentation.

    If a two-tuple is provided, the first item is used as the database
    representation and the second the human-readable presentation.

    If a triple is provided, the first item is the database
    representation, the second a valid Python identifier that can be
    used as a readable label in code, and the third the human-readable
    presentation. This is most useful when the database representation
    must sacrifice readability for some reason: to achieve a specific
    ordering, to use an integer rather than a character field, etc.

    Regardless of what representation of each choice is originally
    given, when iterated over or indexed into, a ``Choices`` object
    behaves as the standard Django choices list of two-tuples.

    If the triple form is used, the Python identifier names can be
    accessed as attributes on the ``Choices`` object, returning the
    database representation. (If the single or two-tuple forms are
    used and the database representation happens to be a valid Python
    identifier, the database representation itself is available as an
    attribute on the ``Choices`` object, returning itself.)

    Option groups can also be used with ``Choices``; in that case each
    argument is a tuple consisting of the option group name and a list
    of options, where each option in the list is either a string, a
    two-tuple, or a triple as outlined above.

    """

    def __init__(self, *choices):
        # list of choices expanded to triples - can include optgroups
        self._triples = []
        # list of choices as (db, human-readable) - can include optgroups
        self._doubles = []
        # dictionary mapping db representation to human-readable
        self._display_map = {}
        # dictionary mapping Python identifier to db representation
        self._identifier_map = {}
        # set of db representations
        self._db_values = set()

        self._process(choices)


    def _store(self, triple, triple_collector, double_collector):
        self._identifier_map[triple[1]] = triple[0]
        self._display_map[triple[0]] = triple[2]
        self._db_values.add(triple[0])
        triple_collector.append(triple)
        double_collector.append((triple[0], triple[2]))


    def _process(self, choices, triple_collector=None, double_collector=None):
        if triple_collector is None:
            triple_collector = self._triples
        if double_collector is None:
            double_collector = self._doubles

        store = lambda c: self._store(c, triple_collector, double_collector)

        for choice in choices:
	    if isinstance(choice, (list, tuple)):
		if len(choice) == 3:
		    store(choice)
		elif len(choice) == 2:
		    if isinstance(choice[1], (list, tuple)):
			# option group
			group_name = choice[0]
			subchoices = choice[1]
			tc = []
			triple_collector.append((group_name, tc))
			dc = []
			double_collector.append((group_name, dc))
			self._process(subchoices, tc, dc)
		    else:
			store((choice[0], choice[0], choice[1]))
		else:
		    raise ValueError(
			"Choices can't take a list of length %s, only 2 or 3"
			% len(choice)
		    )
            else:
		store((choice, choice, choice))


    def __len__(self):
	return len(self._doubles)

    def __iter__(self):
	return iter(self._doubles)

    def __getattr__(self, attname):
	try:
	    return self._identifier_map[attname]
	except KeyError:
	    raise AttributeError(attname)


    def __getitem__(self, key):
        return self._display_map[key]


    def __add__(self, other):
        if isinstance(other, self.__class__):
            other = other._triples
        else:
            other = list(other)
        return Choices(*(self._triples + other))


    def __radd__(self, other):
        # radd is never called for matching types, so we don't check here
        other = list(other)
        return Choices(*(other + self._triples))


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._triples == other._triples
        return False


    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join(("%s" % repr(i) for i in self._triples))
            )


    def __contains__(self, item):
        return item in self._db_values


    def __deepcopy__(self, memo):
        return self.__class__(*copy.deepcopy(self._triples, memo))


class AutoCreatedField(models.DateTimeField):
    """
    A DateTimeField that automatically populates itself at
    object creation.
    By default, sets editable=False, default=timezone.now (fixes timezone)
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', now)
        super(AutoCreatedField, self).__init__(*args, **kwargs)

    def pre_save(self, instance, add):
	val = now()
	if add:
	    setattr(instance, self.attname, val)
	return val
	
#===============================================================================
class AutoLastModifiedField(AutoCreatedField):
    """
    A DateTimeField that updates itself on each save() of the model.
    By default, sets editable=False and default=datetime.now.
    """
    def pre_save(self, model_instance, add):
        value = now()
        setattr(model_instance, self.attname, value)
        return value
	
#===============================================================================
# def get_attr_value(att, instance):
#     if hasattr(att, '__call__'):
#         return att(instance)
#     else:
# 	attr_val = getattr(instance, att)
# 	return attr_val


def crop_string(val, max_len):
    """ always ensures the len of val < max_len"""
    return val[:max_len]
    
class AutoSlugField(models.CharField):
    
    def __init__(self, *args, **kwargs):
	kwargs['max_length'] = kwargs.get('max_length', 250)
	self.source_from = kwargs.pop('source_from',None)
	kwargs['unique'] = False # never enforce uniqueness
	kwargs.setdefault('db_index',True)	
	super(models.CharField,self).__init__(*args,**kwargs)
	
	
    def pre_save(self, instance, add):

	
	# if instance.source_from:
	#     v = get_attr_value(instance.source_from(),instance)
	# logger.critical("%s" % instance.source_from)

    	val = self.value_from_object(instance)
	
    	if not val and instance.source_from:
	    val = getattr(instance, instance.source_from)
	    
	v = val
	if val:
	    val = slugify.slugify(val)
	else:
	    val = None	    
	    if not self.blank:
		val = instance._meta.module_name
    	    elif not self.null:
    		val = ''
    	if val and self.max_length:
    	   val = crop_string(val, self.max_length)

    	setattr(instance, self.attname, val)
    	return val	   


#=========================================== BEGIN IMAGE FIELD ===========================================
from .conf import BaseImageFieldConf
def image_file_path( instance, filename=None, image = None, width=None, height=None, ext=None):
    tmp_dirs = [getattr(instance, "STORAGE_DIR", BaseImageFieldConf.STORAGE_DIR), instance._meta.app_label, instance._meta.object_name.lower()]
    tmp_dirs.append(os.path.dirname(filename))
    filename = os.path.basename(filename)

    if not filename:
        # Filename already stored in database
        filename = image.name
        if ext:
            # An extension was provided, probably because the thumbnail
            # is in a different format than the file. Use it. Because it's
            # only enabled if AVATAR_HASH_FILENAMES is true, we can trust
            # it won't conflict with another filename ext and config.HASH_FILENAMES:
            # An extension was provided, probably because the thumbnail
            # is in a different format than the file. Use it. Because it's
            # only enabled if AVATAR_HASH_FILENAMES is true, we can trust
            # it won't conflict with another filename
            (root, oldext) = os.path.splitext(filename)
            filename = root + "." + ext
    else:
        # File doesn't exist yet
        #if config.AVATAR_HASH_FILENAMES:

	(root, ext) = os.path.splitext(filename)

	filename = hashlib.md5(force_bytes(filename)).hexdigest()
	filename = filename + ext
    if width and height:
	tmp_dirs.extend( [width, height] )

    tmp_dirs.append(os.path.basename(filename))

    return os.path.join(*tmp_dirs)

def process_image_data(image_file, **kwargs):

    from PIL import Image
    from cStringIO import StringIO
    from django.utils import six
    from django.core.files.base import ContentFile
    import math
    #image_file = kwargs.get('data')
    image = Image.open(StringIO(image_file.read()))

    if kwargs.get('resized', False):
	width, height = kwargs.get('width'), kwargs.get('height')
	image = image.resize( (width, height), Image.ANTIALIAS)

    if kwargs.get('cropped'):
	left, top = kwargs.get('x'), kwargs.get('y')
	right, bottom = left + kwargs.get('width'), top + kwargs.get('height')
	box = (int(left), int(top), int(right), int(bottom))
	image = image.crop(box)
	
    img_data = six.BytesIO()
    image.save(img_data, kwargs.get('format', 'jpeg'), quality=85)
    image_file = ContentFile(img_data.getvalue())
	
    return image_file

class BaseImageField(models.ImageField):    
    def __init__(self, *args, **kwargs):
	from django.core.files.storage import get_storage_class
	config = self._get_config()
	# self.width = kwargs.get('width', self.config.)
	# self.height = kwargs.get('height', config.BASEIMAGE_DEFAULT_SIZE)
        kwargs['upload_to'] = kwargs.get('upload_to', image_file_path)
	kwargs['storage'] =  get_storage_class(config.STORAGE)(**config.STORAGE_PARAMS)
	kwargs['blank'] = True
        super(BaseImageField, self).__init__(*args, **kwargs)

    def _get_config(self):
	return BaseImageFieldConf

#===================================================================================
class NullCharField(six.with_metaclass(models.SubfieldBase, models.CharField)):
    """
    CharField that stores '' as None and returns None as ''
    Useful when using unique=True and forms. Implies null==blank==True.
    When a ModelForm with a CharField with null=True gets saved, the field will
    be set to '': https://code.djangoproject.com/ticket/9590
    This breaks usage with unique=True, as '' is considered equal to another
    field set to ''.
    """
    description = "CharField that stores '' as None and returns None as ''"

    def __init__(self, *args, **kwargs):
        if not kwargs.get('null', True) or not kwargs.get('blank', True):
            raise ImproperlyConfigured(
                "NullCharField implies null==blank==True")
        kwargs['null'] = kwargs['blank'] = True
        super(NullCharField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        val = super(NullCharField, self).to_python(value)
        return val if val is not None else u''

    def get_prep_value(self, value):
        prepped = super(NullCharField, self).get_prep_value(value)
        return prepped if prepped != u"" else None

    def deconstruct(self):
        """
        deconstruct() is needed by Django's migration framework
        """
        name, path, args, kwargs = super(NullCharField, self).deconstruct()
        del kwargs['null']
        del kwargs['blank']
        return name, path, args, kwargs
