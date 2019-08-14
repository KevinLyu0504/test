from django.db import models
from datetime import datetime

class WPworld(models.Model):

    wp_world = models.CharField(max_length=200)
    world_summary = models.CharField(max_length=200)
    world_slug = models.CharField(max_length=200, default=1)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "World"

    def __str__(self):
        return self.wp_world
		
class WPseries(models.Model):
    wp_series = models.CharField(max_length=200)

    wp_world = models.ForeignKey(WPworld, default=1, verbose_name="World", on_delete=models.SET_DEFAULT)
    series_summary = models.CharField(max_length=200)

    class Meta:
        # otherwise we get "WP series in admin"
        verbose_name_plural = "series"

    def __str__(self):
        return self.wp_series
		

class WP(models.Model):
    wp_title = models.CharField(max_length=200)
    wp_content = models.TextField()
    wp_published = models.DateTimeField('date published')
    #https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
    wp_series = models.ForeignKey(WPseries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
    wp_slug = models.CharField(max_length=200, default=1)
    wp_image = models.ImageField(upload_to='images', blank=True)
    def __str__(self):
        return self.wp_title
