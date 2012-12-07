from london.apps.admin import modules

from images.models import Image
from images import signals


class ImageForm(modules.BaseModuleForm):

    class Meta:
        model = Image
        exclude = ('existing_thumbnails', 'image_center', 'created')

    def default_context(self, *args, **kwargs):
        context = super(ImageForm, self).default_context(*args, **kwargs)
        
        context['object_verbose_name'] = self._meta.model._meta.verbose_name
        context['object_verbose_name_plural'] = self._meta.model._meta.verbose_name_plural
        return context
        
    def get_initial(self, initial=None):
        initial = initial or super(ImageForm, self).get_initial(initial)
        signals.image_form_initialize.send(sender=self, initial=initial)
        return initial
    
    def save(self, commit=True, force_new=False):
        signals.image_form_pre_save.send(sender=self)
        obj = super(ImageForm, self).save(commit, force_new)
        return obj