from django.db import models

# Create your models here.
#

class Crop(models.Model):
    crop_nitrogen = models.FloatField(blank=True, null=True)
    crop_phosphorous = models.FloatField(blank=True, null=True)
    crop_potassium = models.FloatField(blank=True, null=True)
    crop_temperature = models.FloatField(blank=True, null=True)
    crop_rainfall = models.FloatField(blank=True, null=True)
    crop_humidity = models.FloatField(blank=True, null=True)
    crop_ph = models.FloatField(blank=True, null=True)
    crop_level = models.CharField(max_length=100) # might get error here

    def __str__(self):
        return self.crop_level

    class Meta:
        ordering = ['crop_level']

class kagel_crop(models.Model):
    id = models.IntegerField(primary_key=True)
    image_path = models.CharField(max_length=100, blank=True, null=True)
    crop_name = models.CharField(max_length=100, blank=True, null=True)
    crop_label = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.crop_name

    class Meta:
        ordering = ['crop_name']
