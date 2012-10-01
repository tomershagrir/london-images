from jinja2 import Template
from london.utils.safestring import mark_safe
from london import forms
from london.templates import render_to_string
from images.models import Image

from app_settings import SITE_SPECIFIC_IMAGES 


class ImagesWidget(forms.Widget):
    
    class Media:
        js = ('images:scrollable','images:images')
        css = {
               'all': ('styles/images:basic/',)
        }

    image_height = '50px'
    images_per_row = 6
    
    def partition(self, lst,n): return [lst[:n]] + self.partition(lst[n:],n) if lst and n else []

    def render(self, name, value, attrs=None):
        images = Image.query().active()
        if 'site' in self.attrs and self.attrs['site'] and WIDGET_SITE_SPECIFIC_IMAGES:
            images = images.filter(pk__in = [str(pk) for pk in self.attrs['site']['images'].values_list('pk', flat=True)])
        rows = self.partition(list(images),self.images_per_row)
        return render_to_string('image_list.html', {'images':rows, 'image_height':self.image_height })

    def render_label(self, name, label):
        return mark_safe(u'<h2><span>%s</span></h2>' % name)