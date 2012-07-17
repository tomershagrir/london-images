from london.db import models
from london.apps.sites.models import Site

from images.thumbnails import thumbs_getattr


class Image(models.Model):
    """
    Image model to store images
    """
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True, db_index=True, blank=True)
    is_public = models.BooleanField(default=True, db_index=True, blank=True)
    keywords = models.ListField(blank=True, null=True)
    alt_text = models.CharField(max_length=100,blank=True,null=True)
    copyright = models.CharField(max_length=100, blank=True)
    image_center = models.CharField(max_length=20, blank=True)
    existing_thumbnails = models.TextField(blank=True)
    image = models.ImageField()
    sites = models.ManyToManyField(Site, blank=True, related_name='images')
    
    __getattr__ = thumbs_getattr('image')
    
    def get_image_center_for_200(self):
        if not self['image_center'] or not self['image']:
            return ''
        center = map(int, self['image_center'].split(','))
        factor = (min(200.0, self['image'].height, self['image'].width) /
                  max([self['image'].height,self['image'].width]))
        return '%s,%s'%(center[0] * factor, center[1] * factor)

    def __unicode__(self):
        return self['name']

    def all_sites(self):
        return Site.query()  