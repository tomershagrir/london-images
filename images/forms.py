from london import forms
from images.models import Image

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image

    def default_context(self, *args, **kwargs):
        return {
            'object_verbose_name': self._meta.model._meta.verbose_name,
            'object_verbose_name_plural': self._meta.model._meta.verbose_name_plural
        }

