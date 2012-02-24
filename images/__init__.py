import os
from london.apps.ajax import site
from pages.signals import page_form_initialize
from london import forms
from widgets import ImagesWidget


site.register_scripts_dir('images', os.path.join(os.path.dirname(__file__), 'scripts'))
site.register_styles_dir('images', os.path.join(os.path.dirname(__file__), 'styles'))


def add_page_fields(sender):
    form = sender
    form.fields['images'] = forms.Field(name='images', widget=ImagesWidget)

page_form_initialize.connect(add_page_fields)