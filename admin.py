from london.apps import admin
from london.apps.images.models import Image

class ModuleImage(admin.CrudModule):
    model = Image
    list_display = ('name','site','keywords','image',)

class AppRedirects(admin.AdminApplication):
    title = 'Image'
    modules = (ModuleImage,)

