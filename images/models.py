from london.db import models
from london.apps.sites.models import Site

class Image(models.Model):
    """
    """
    name = models.CharField(max_length=100)
    site = models.ManyToManyField(Site,related_name='images')
    keywords = models.ListField(blank=True, null=True)
    alt_text = models.CharField(max_length=100,blank=True,null=True)
    image = models.ImageField()

    def __unicode__(self):
        return self.name


