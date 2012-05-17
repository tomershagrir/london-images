import os
from london.apps.ajax import site
import london
from widgets import ImagesWidget

site.register_scripts_dir('images', os.path.join(os.path.dirname(__file__), 'scripts'))
site.register_styles_dir('images', os.path.join(os.path.dirname(__file__), 'styles'))

def add_image_field_to_sender_form(sender):
    form = sender
    form.fields['images'] = london.forms.Field(name='images', widget=ImagesWidget(), required=False)