from jinja2 import Template
from london.utils.safestring import mark_safe
from london import forms
from london.templates import render_to_string
from models import Image



class ImagesWidget(forms.Widget):

    image_height = '50px'
    images_per_row = 6

    def render(self, name, value, attrs=None):
        # TODO: filter by current site
        ## the current site is in the request. How do we access the request from here?
        ## images = site['images']
        images = Image.query()
        return render_to_string('image_list.html', {'images':images, 'image_height':self.image_height })


