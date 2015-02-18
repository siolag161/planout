from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Hidden
from crispy_forms.bootstrap import AppendedText, InlineCheckboxes, FormActions
from django.template.defaultfilters import filesizeformat

#from .conf import AvatarConf as config
from .conf import settings as config

import os.path

import logging
logger = logging.getLogger('werkzeug')

class UploadAvatarForm(forms.Form):
    avatar = forms.ImageField(label=("Avatar"))
    avatar_src = forms.Field(required=False)
    avatar_data = forms.Field(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
	super(UploadAvatarForm, self).__init__(*args, **kwargs)
 
	helper = FormHelper()
	helper.form_show_labels = False
	helper.layout = Layout(
	    Div(
		Field('avatar_src', type="hidden", css_class="avatar-src"),
		Field('avatar_data', type="hidden", css_class="avatar-data", required=False),

		Field('avatar', id='avatarInput', css_class="avatar-input", required=False),
		css_class="avatar-upload",
	    ),
	)
        self.helper = helper

    def clean_avatar(self):
        data = self.cleaned_data['avatar']
	if data.size > config.AVATAR_MAX_SIZE:
	    error = _("Your file is too big (%(size)s), "
		      "the maximum allowed size is %(max_valid_size)s")

	    raise forms.ValidationError(error % {
		 'size': filesizeformat(data.size),
		'max_valid_size': filesizeformat(config.AVATAR_MAX_SIZE)
	    })
	if config.AVATAR_ALLOWED_FILE_EXTS:
            root, ext = os.path.splitext(data.name.lower())
            if ext not in config.AVATAR_ALLOWED_FILE_EXTS:
                valid_exts = ", ".join(config.AVATAR_ALLOWED_FILE_EXTS)
                error = _("%(ext)s is an invalid file extension. "
                          "Authorized extensions are : %(valid_exts_list)s")
                raise forms.ValidationError(error %
                                            {'ext': ext,
                                             'valid_exts_list': valid_exts})
        # return
