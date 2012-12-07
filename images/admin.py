from london.apps import admin
from london.urls import patterns
from london.http import JsonResponse
from london.apps.sites.models import Site
from london.apps.admin.app_settings import CURRENT_SITE_FILTER

from images.models import Image
from images.forms import ImageForm
from images.app_settings import WIDGET_SITE_SPECIFIC_IMAGES 


class ModuleImage(admin.CrudModule):
    model = Image
    form = ImageForm
    list_display = ('name','site','keywords','image',)
    exclude = ('existing_thumbnails', 'image_center', 'created')
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
            
            site = None
            if request.session[CURRENT_SITE_FILTER] != '':
                site = Site.query().get(pk = request.session[CURRENT_SITE_FILTER])
            
            queryset = Image.query()
            for bit in bits:
                if site and WIDGET_SITE_SPECIFIC_IMAGES:
                    queryset = queryset.filter(pk__in = [str(pk) for pk in site['images'].values_list('pk', flat=True)])
                queryset = queryset.filter_if_any(*[{lookup: bit} for lookup in lookups])
            return JsonResponse(queryset.values('name'))
        return JsonResponse()


class AppImages(admin.AdminApplication):
    title = 'Image'
    modules = (ModuleImage,)