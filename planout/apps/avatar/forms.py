from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, InlineCheckboxes, FormActions
from .conf import AvatarConf as config
# from .widgets import AvatarWidget

# class AvatarField(forms.ImageField):
#     widget = AvatarWidget
    

#     def __init__(self, **defaults):
#         self.width = defaults.pop('width', config.AVATAR_DEFAULT_WIDTH)
#         self.height = defaults.pop('height', config.AVATAR_DEFAULT_HEIGHT)

	
#         super(AvatarField, self).__init__(**defaults)

#     def to_python(self, data):
#         super(AvatarField, self).to_python(data['file'])
#         return data

#     def widget_attrs(self, widget):
	
#         return {'width': self.width, 'height': self.height, 'id': 'avatar-id'}

class UploadAvatarForm(forms.Form):
    # avatar = forms.ImageField(label=("Avatar"))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
    	# helper = FormHelper()
    	# helper.form_show_labels = False
        # helper.layout = Layout(
    	#     SmallFileField('main_image', 'second_image')
    	# )
        super(UploadAvatarForm, self).__init__(*args, **kwargs)
    pass
