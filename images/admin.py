from london.apps import admin
from london.urls import patterns
from images.models import Image
from london.http import JsonResponse

class ModuleImage(admin.CrudModule):
    model = Image
    list_display = ('name','site','keywords','image',)

    def get_urls(self):
        extra = patterns('',
            (r'^filter_images/$', self.filter_images, {}),
        )
        urls = super(ModuleImage, self).get_urls()
        extra.extend(urls)
        return extra

    #def filter_images(self,app,request,module):
    def filter_images(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            return JsonResponse(Image.query(keywords__contains=query).values('name'))
        return JsonResponse()


class AppImages(admin.AdminApplication):
    title = 'Image'
    modules = (ModuleImage,)