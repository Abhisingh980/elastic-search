from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import Crop, kagel_crop

@registry.register_document
class CropDocument(Document):
    class Index:
        name = 'crops'
        settings = {'number_of_shards': 8,
                    'number_of_replicas': 0}

    class Django:
        model = Crop
        fields = [
            'crop_nitrogen',
            'crop_phosphorous',
            'crop_potassium',
            'crop_temperature',
            'crop_rainfall',
            'crop_humidity',
            'crop_ph',
            'crop_level',
        ]
