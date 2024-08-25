from django.shortcuts import render
from .models import Crop, kagel_crop
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .document import CropDocument
from elasticsearch_dsl.query import MultiMatch

# Create your views here.

def elastic_helper(request):

    # Get all crops from the database and order them by crop level
    crop = Crop.objects.all().order_by('crop_level')
    kaggle_crop_detail = kagel_crop.objects.all().order_by('id')

    if request.method == 'GET':
        search_text_query = request.GET.get('esearch', None)
        if search_text_query:
            # search for crops
            search = CropDocument.search().query(
                MultiMatch(query=search_text_query, fields=
                    ['crop_level'])
            )
            crop = search

    return crop, kaggle_crop_detail

def basic_search(request):
    crop = Crop.objects.all().order_by('crop_level')
    kaggle_crop_detail = kagel_crop.objects.all().order_by('id')

    if request.method == 'GET':
        search_text_query = request.GET.get('esearch', None)
        if search_text_query:
            crop = Crop.objects.filter(crop_level__icontains=search_text_query)
            kaggle_crop_detail = kagel_crop.objects.filter(crop_name__icontains=search_text_query)
        else:
            crop= crop
            kaggle_crop_detail = kaggle_crop_detail

    return crop, kaggle_crop_detail



def search(request):
    crop, kaggle_crop_detail = elastic_helper(request)

    # paginator
    paginator_crops = Paginator(crop, 6)
    paginator_kaggle = Paginator(kaggle_crop_detail, 6)

    # Get the page number from the request for each set
    page_number_crops = request.GET.get('page_crops', 1)
    page_number_kaggle = request.GET.get('page_kaggle', 1)

    # Get the page for crops
    try:
        crops = paginator_crops.get_page(page_number_crops)
    except PageNotAnInteger:
        crops = paginator_crops.get_page(1)
    except EmptyPage:
        crops = paginator_crops.page(paginator_crops.num_pages)

    # Get the page for kaggle_crop_detail
    try:
        kaggle_crop_detail = paginator_kaggle.get_page(page_number_kaggle)
    except PageNotAnInteger:
        kaggle_crop_detail = paginator_kaggle.get_page(1)
    except EmptyPage:
        kaggle_crop_detail = paginator_kaggle.page(paginator_kaggle.num_pages)

    # Calculate the page range for crops
    page_range_crops = paginator_crops.page_range
    current_page_crops = crops.number
    total_pages_crops = paginator_crops.num_pages
    total_pages_kaggle = paginator_kaggle.num_pages

    start_page_crops = max(current_page_crops - 4, 1)
    end_page_crops = min(current_page_crops + 4, total_pages_crops)

    if end_page_crops - start_page_crops < 9:
        if start_page_crops > 1:
            end_page_crops = min(start_page_crops + 9, total_pages_crops)
        else:
            start_page_crops = max(end_page_crops - 9, 1)

    page_range_to_show_crops = list(range(start_page_crops, end_page_crops + 1))

    # Calculate the page range for kaggle_crop_detail
    page_range_kaggle = paginator_kaggle.page_range
    current_page_kaggle = kaggle_crop_detail.number
    total_pages_kaggle = paginator_kaggle.num_pages

    start_page_kaggle = max(current_page_kaggle - 4, 1)
    end_page_kaggle = min(current_page_kaggle + 4, total_pages_kaggle)

    if end_page_kaggle - start_page_kaggle < 9:
        if start_page_kaggle > 1:
            end_page_kaggle = min(start_page_kaggle + 9, total_pages_kaggle)
        else:
            start_page_kaggle = max(end_page_kaggle - 9, 1)

    page_range_to_show_kaggle = list(range(start_page_kaggle, end_page_kaggle + 1))

    # Prepare context with pagination information
    context = {
        'total_page_number_crops': total_pages_crops,
        'total_page_number_kaggle': total_pages_kaggle,
        'crops': crop,
        'kaggle_crops': kaggle_crop_detail,
        'page_range_to_show_crops': page_range_to_show_crops,
        'page_range_to_show_kaggle': page_range_to_show_kaggle,
        'has_previous_crops': crops.has_previous(),
        'has_next_crops': crops.has_next(),
        'previous_page_number_crops': crops.previous_page_number() if crops.has_previous() else None,
        'next_page_number_crops': crops.next_page_number() if crops.has_next() else None,
        'has_previous_kaggle': kaggle_crop_detail.has_previous(),
        'has_next_kaggle': kaggle_crop_detail.has_next(),
        'previous_page_number_kaggle': kaggle_crop_detail.previous_page_number() if kaggle_crop_detail.has_previous() else None,
        'next_page_number_kaggle': kaggle_crop_detail.next_page_number() if kaggle_crop_detail.has_next() else None,
        # Add other context variables as needed
    }


    return render(request, 'search.html',context)
