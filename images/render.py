from models import Image
import re

class ImagesRender():

    def render(self, source):
        return self._render_images(source)

    def _render_images(self, source):
        regex = re.compile("\{IMAGE:(.*)\}")
        list_image = regex.findall(source)

        for name in list_image:
            try:
                obj = Image.query().filter(name=name).get()
                img = '<img src="%s" />' % obj['image'].url
                source = source.replace("{IMAGE:%s}" % name, img)
            except:
                continue
        return source

