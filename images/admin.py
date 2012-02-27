from london.apps import admin
from london.urls import patterns
from models import Image
from forms import ImageForm
from london.http import JsonResponse

class ModuleImage(admin.CrudModule):
    model = Image
    list_display = ('name','site','keywords','image',)
    form = ImageForm

    def get_urls(self):
        extra = patterns('',
            (r'^filter_images/$', self.filter_images, {}),
        )
        urls = super(ModuleImage, self).get_urls()
        extra.extend(urls)
        return extra

    def filter_images(self,app,request,module):
        query = request.GET.get('q')
        if query:
            return JsonResponse(Image.query(keywords__contains=query).values('name'))
        return JsonResponse()




class AppImages(admin.AdminApplication):
    title = 'Image'
    modules = (ModuleImage,)

