import os
from pages.signals import page_form_initialize
from london import forms
from london.utils.safestring import mark_safe
from models import Image
from london.apps.ajax import site


site.register_scripts_dir('images', os.path.join(os.path.dirname(__file__), 'scripts'))


html = \
'''
<hr>
<div style="margin-top:10px" id="images-container">
    %s
</div>
<script src="/ajax/scripts/images:images/" type="text/javascript"></script>
<script type="text/javascript">
    jQuery(document).ready(function(){
        Images.init();
    });
</script>
'''

height = 50

def toHtml(img):
    return '<a style="cursor:pointer"><img src="%s" height="%d" alt="%s" title="%s"></a>' % \
           (img['image'].url,height,img['alt_text'] or '',img['name'])

class ImagesWidget(forms.Widget):

    def render(self, name, value, attrs=None):
        images = Image.query()
        anchors = ' '.join([toHtml(im) for im in images])
        return mark_safe(html % anchors)

    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value



def add_page_fields(sender):
    form = sender
    form.fields['images'] = forms.Field(name='images', widget=ImagesWidget)

page_form_initialize.connect(add_page_fields)