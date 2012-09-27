import os

import london
from london.apps.ajax import site
from london.apps.admin.app_settings import CURRENT_SITE_FILTER
from london.apps.sites.models import Site

from images.widgets import ImagesWidget


site.register_scripts_dir('images', os.path.join(os.path.dirname(__file__), 'scripts'))
site.register_styles_dir('images', os.path.join(os.path.dirname(__file__), 'styles'))

def add_image_field_to_sender_form(sender):
    form = sender
    site = None
    if form.request.session[CURRENT_SITE_FILTER] != '':
        site = Site.query().get(pk = form.request.session[CURRENT_SITE_FILTER])
    form.fields['images'] = london.forms.Field(name='images', widget=ImagesWidget({'site':site}), required=False)