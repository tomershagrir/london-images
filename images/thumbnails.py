import re, math
from os import path

try:
    import Image
    import ImageOps
except ImportError:
    from PIL import Image
    from PIL import ImageOps

def thumbs_getattr(field_name, default_url=None):
    GET_THUMB_PATTERN = re.compile(r'^get_%s_(\d+x\d+|original)(|_[a-z_]+)_(url|filename)$' % field_name)

    def _getattr(self, name):
        """
        Deploys dynamic methods for on-demand thumbnails creation with any
        size.

        Syntax::

            get_photo_[original|WIDTHxHEIGHT][_crop|_stretch][_gray]_[METHOD]

        Where *WIDTH* and *HEIGHT* are the pixels of the new thumbnail and
        *METHOD* can be ``url`` or ``filename``.

        Example usage::

            >>> photo.get_image_320x240_url()
            u"http://media.example.net/photos/2008/02/26/example_320x240.jpg"
            >>> photo.get_image_320x240_filename()
            u"/srv/media/photos/2008/02/26/example_320x240.jpg"
            >>> photo.get_image_320x240_crop_url()
            u"/srv/media/photos/2008/02/26/example_320x240_crop.jpg"
            >>> photo.get_image_320x240_stretch_gray_url()
            u"/srv/media/photos/2008/02/26/example_320x240_stretch_gray.jpg"
            >>> photo.get_image_original_url()
            u"http://media.example.net/photos/2008/02/26/example.jpg"
            
        """
        field_value = self[field_name]
        if not field_value:
            raise AttributeError, name
        match = re.match(GET_THUMB_PATTERN, name)
        if match is None:
            raise AttributeError, name
        #width, height, extra, method = match.groups()
        size_group, extra, method = match.groups()

        if size_group != 'original':
            width, height = size_group.split('x')
            size = int(width), int(height)
            thumb_name = '%sx%s%s'%(size[0], size[1], extra)
        else:
            size = None
            thumb_name = '%s' % extra

        def get_thumbnail_filename():
            try:
                file, ext = path.splitext(field_value.file.name)
                if size is None:
                    return file + ext
                return file + '_%sx%s%s%s'%(size[0], size[1], extra, ext)
            except IOError:
                return None

        def get_thumbnail_url():
            url, ext = path.splitext(field_value.url)
            if size is None:
                return url + ext
            return url + '_%sx%s%s%s'%(size[0], size[1], extra, ext)

        try:
            thumbnail = get_thumbnail_filename()
            if thumbnail and (not path.exists(thumbnail) or thumb_name not in (self['existing_thumbnails'] or '').split(',')):
                img = Image.open(field_value.file.name)
                
                if '_crop' in extra:
                    sq = int(math.ceil(float(max(img.size)) / min(img.size) * max(size)))
                    new_size = (sq, sq)

                    if getattr(self, 'image_center', None):
                        center = map(int, self.image_center.strip().split(',')[:2])
                    else:
                        center = (img.size[0] / 2, img.size[1] / 2)
                    
                    crop_q = size[0]/float(size[1])
                    image_q = img.size[0]/float(img.size[1])
                    
                    if crop_q < image_q:
                        crop_h = img.size[1]
                        crop_w = int(crop_h*float(crop_q))
                    else:
                        crop_w = img.size[0]
                        crop_h = int(crop_w/float(crop_q))
                    
                    left = center[0] - crop_w/2
                    if left < 0:
                        left = 0
                    elif left + crop_w > img.size[0]:
                        left = img.size[0] - crop_w
                    right = left + crop_w

                    top = center[1] - crop_h / 2
                    if top < 0:
                        top = 0
                    elif top + crop_h > img.size[1]:
                        top = img.size[1] - crop_h
                    bottom = top + crop_h
                    
                    box = (left, top, right, bottom)
                    img = img.crop(box)
                    img = img.resize(size, Image.ANTIALIAS)
                elif '_stretch' in extra:
                    q = float(img.size[0]) / img.size[1]
                    new_size = size
                    if 0 in size:
                        if size[0] == 0:
                            new_size = (int(size[1]*q), size[1])
                        if size[1] == 0:
                            new_size = (size[0], int(size[0]/q))
                    img = img.resize(new_size, Image.ANTIALIAS)
                else:
                    if size:
                        img.thumbnail(size, Image.ANTIALIAS)

                if '_gray' in extra:
                    img = ImageOps.grayscale(img)

                try: # XXX
                    # fixing "IOError: cannot write mode P as JPEG"
                    if img.format == 'JPEG' and img.mode != "RGB": 
                        img = img.convert("RGB")
                    if img.format == 'JPEG':
                        img.save(thumbnail, 'JPEG', quality=100)
                    else:
                        img.save(thumbnail) # saving
                except KeyError:
                    return '' # it's better to return empty than to crash the website

                # Stores this thumbnail was made to make possible to force recreation
                existing_thumbnails = (self['existing_thumbnails'] or '').split(',')
                existing_thumbnails.append(thumb_name)
                self['existing_thumbnails'] = ','.join(set([t.strip() for t in existing_thumbnails if t.strip()]))
                self.save()

            # Closes the file for prevent error like "Too many files open"
            if field_value.file:
                field_value.file.close()
                field_value.file = None

            if method == "url":
                return get_thumbnail_url()
            else:
                return get_thumbnail_filename()
        except (ValueError, IOError):
            if method == 'url' and default_url is not None:
                return default_url % size
            else:
                return ''
    
    return _getattr
