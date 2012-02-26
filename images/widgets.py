from jinja2 import Template
from london.utils.safestring import mark_safe
from london import forms
from london.templates import render_to_string
from models import Image


def partition(lst,n):
    new_lst = [[]]
    row = new_lst[0]
    for element in lst:
        if len(row) == n:
            row = []
            new_lst.append(row)
        row.append(element)
    return new_lst

class ImagesWidget(forms.Widget):

    image_height = '50px'
    images_per_row = 6

    def render(self, name, value, attrs=None):
        images = Image.query()
        lst = partition(images,self.images_per_row)
        return render_to_string('image_list.html', {'images':lst, 'image_height':self.image_height })


