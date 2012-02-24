from jinja2 import Template
from london.utils.safestring import mark_safe
from london import forms
from london.templates import render_to_string
from models import Image


class ImagesWidget(forms.Widget):

    def render(self, name, value, attrs=None):
        images = Image.query()
        return render_to_string('image_list.html', {'images':images})


