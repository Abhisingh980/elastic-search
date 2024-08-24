import pandas as pd
import numpy as np

from .models import Crop, kagel_crop

# Create your views here.

def fill_crop():
    df = pd.read_csv('/Users/abhisingh/elastic_search/elastic/Crop_recommendation.csv')
    for index, row in df.iterrows():
        obj = Crop.objects.create(
            crop_nitrogen=row['N'],
            crop_phosphorous=row['P'],
            crop_potassium=row['K'],
            crop_temperature=row['temperature'],
            crop_rainfall=row['rainfall'],
            crop_humidity=row['humidity'],
            crop_ph=row['ph'],
            crop_level=row['label']
        )
        obj.save()

def cropdetail():
    df = pd.read_csv('/Users/abhisingh/elastic_search/elastic/Crop_details.csv')

    #emplemant try catch block
    for index, row in df.iterrows():
        obj = kagel_crop.objects.create(
            image_path=row['path'],
            # if crop_name is not present in Crop model then try except block
            crop_name=row['crop'],
            crop_label=row['croplabel']
        )
        obj.save()
