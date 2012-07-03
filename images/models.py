from london.db import models
from london.apps.sites.models import Site

from images.thumbnails import thumbs_getattr


class Image(models.Model):
    """
    """
    name = models.CharField(max_length=100)
    sites = models.ManyToManyField(Site, blank=True, related_name='images')
    keywords = models.ListField(blank=True, null=True)
    alt_text = models.CharField(max_length=100,blank=True,null=True)
    existing_thumbnails = models.TextField(blank=True)
    image = models.ImageField()
    
    __getattr__ = thumbs_getattr('image')

    def __unicode__(self):
        return self['name']

    def all_sites(self):
        return Site.query()