from re import VERBOSE
from django.shortcuts import render
from .models import Crop, kagel_crop
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .document import CropDocument, KagelCropDocument
from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search

# Create your views here.

def elastic_helper(request):
    page_number = int(request.GET.get('page', 1))
    search_text_query = request.GET.get('esearch', None)

    # Set the size for pagination
    page_size = 9

    # For crops
    if search_text_query:
        if not search_text_query.isnumeric():
            # Fuzzy search on 'crop_level' for crops and Kaggle crops
            crop_search = CropDocument.search().query(
                MultiMatch(query=search_text_query, fields=['crop_level'], fuzziness='AUTO')
            )
            kaggle_crops_search = KagelCropDocument.search().query(
                MultiMatch(query=search_text_query, fields=['crop_name'], fuzziness='AUTO')
            )
        else:
            # Specific field search for numeric queries
            crop_search = CropDocument.search().query(
                MultiMatch(query=search_text_query, fields=[
                    'crop_ph', 'crop_humidity', 'crop_rainfall',
                    'crop_temperature', 'crop_potassium',
                    'crop_phosphorous', 'crop_nitrogen'
                ])
            )
            # Assuming similar logic for Kaggle crops if needed
            kaggle_crops_search = KagelCropDocument.search().query(
                MultiMatch(query=search_text_query, fields=['crop_level'])
            )
    else:
        # If no search text, fetch all documents
        crop_search = CropDocument.search().query('match_all')
        kaggle_crops_search = KagelCropDocument.search().query('match_all')

    # Apply pagination
    crop_search = crop_search.extra(from_=(page_number - 1) * page_size, size=page_size)
    kaggle_crops_search = kaggle_crops_search.extra(from_=(page_number - 1) * page_size, size=page_size)

    # total page number
    total_page_crop = crop_search.count() // page_size + 1
    total_page_kaggle_crop = kaggle_crops_search.count() // page_size + 1


    # Execute queries
    crops = crop_search.execute()
    kaggle_crops = kaggle_crops_search.execute()

    # Convert results to dictionaries
    crops_data = [hit.to_dict() for hit in crops]
    kaggle_crops_data = [hit.to_dict() for hit in kaggle_crops]


    return crops_data, kaggle_crops_data, total_page_crop, total_page_kaggle_crop



# def basic_search(request):
#     crop = Crop.objects.all().order_by('crop_level')
#     kaggle_crop_detail = kagel_crop.objects.all().order_by('id')

#     if request.method == 'GET':
#         search_text_query = request.GET.get('esearch', None)
#         if search_text_query:
#             crop = Crop.objects.filter(crop_level__icontains=search_text_query)
#             kaggle_crop_detail = kagel_crop.objects.filter(crop_name__icontains=search_text_query)
#         else:
#             crop= crop
#             kaggle_crop_detail = kaggle_crop_detail

#     return crop, kaggle_crop_detail



def search(request):
    crops, kaggle_crops, total_page_crop, total_page_kagel_crop = elastic_helper(request)

    context = {
        'crops': crops,
        'kaggle_crops': kaggle_crops,
        'page_number': int(request.GET.get('page', 1)),
        'total_page_crop': total_page_crop,
        'total_page_kagel_crop': total_page_kagel_crop
    }

    return render(request, 'search.html', context)
