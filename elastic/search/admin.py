from django.contrib import admin

# Register your models here.
from .models import Crop, kagel_crop

admin.site.register(Crop)
admin.site.register(kagel_crop)
