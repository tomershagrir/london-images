from london.apps import admin
from london.urls import patterns
from london.http import JsonResponse

from images.models import Image
from images.forms import ImageForm


class ModuleImage(admin.CrudModule):
    model = Image
    form = ImageForm
    list_display = ('name','site','keywords','image',)
    exclude = ('existing_thumbnails', 'image_center')
    search_fields = ('name','keywords','alt_text','copyright')

    def get_urls(self):
        extra = patterns('',
            (r'^filter_images/$', self.filter_images, {}),
        )
        urls = super(ModuleImage, self).get_urls()
        extra.extend(urls)
        return extra

    def filter_images(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            if self.search_fields is None:
                self.search_fields = ('keywords',)
            lookups = ["%s__icontains" % field for field in self.search_fields]
            bits = query.split()
            for bit in bits:
                queryset = Image.query().filter_if_any(*[{lookup: bit} for lookup in lookups])
            return JsonResponse(queryset.values('name'))
        return JsonResponse()


class AppImages(admin.AdminApplication):
    title = 'Image'
    modules = (ModuleImage,)