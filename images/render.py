from models import Image
import re

class ImagesRender():

    def render(self, source):
        return self._render_images(source)

    def _render_images(self, source):
        regex = re.compile("\{IMAGE:(.*?)\}")
        list_image = regex.findall(source)

        for name in list_image:
            try:
                obj = Image.query().filter(name=name).get()
                alt = None
                if obj['alt_text']:
                    alt = ' alt="%s"' % obj['alt_text']
                img = '<img src="%s"%s />' % (obj['image'].url, alt)
                source = source.replace("{IMAGE:%s}" % name, img)
            except:
                continue
        return source

