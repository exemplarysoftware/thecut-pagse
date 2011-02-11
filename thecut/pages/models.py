from django.db import models
from thecut.pages.utils import generate_unique_url
from thecut.core.managers import QuerySetManager
from thecut.core.models import AbstractSiteResource, AbstractSitesResource


class Page(AbstractSiteResource):
    """Generic page."""
    url = models.CharField(max_length=100, db_index=True,
        help_text='Example: /my-page')
    
    objects = QuerySetManager()
    
    class Meta(AbstractSiteResource.Meta):
        unique_together = ['url', 'site']
    
    def get_absolute_url(self):
        return self.url
    
    def save(self, *args, **kwargs):
        if not self.url:
            self.url = generate_unique_url(self.title, Page,
                queryset=Page.objects.filter(site=self.site))
        if not self.url.startswith('/'):
            self.url = '/%s' %(self.url)
        super(Page, self).save(*args, **kwargs)


class SitesPage(AbstractSitesResource):
    """Generic page, which can be associated with multiple sites."""
    url = models.CharField(max_length=100, db_index=True, unique=True,
        help_text='Example: /my-page')
    
    objects = QuerySetManager()
    
    def get_absolute_url(self):
        return self.url
    
    def save(self, *args, **kwargs):
        if not self.url:
            self.url = generate_unique_url(self.title, SitesPage,
                queryset=SitesPage.objects.all())
        if not self.url.startswith('/'):
            self.url = '/%s' %(self.url)
        super(SitesPage, self).save(*args, **kwargs)

