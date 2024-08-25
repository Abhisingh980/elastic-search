from django.shortcuts import render
from .models import Crop, kagel_crop
from django.core.paginator import Paginator
# import q
from django.db.models import Q

# Create your views here.





def search(request):
    # Get all crops from the database and order them by crop level
    crop = Crop.objects.all().order_by('crop_level')
    kaggle_crop_detail = kagel_crop.objects.all().order_by('id')

    if request.method == 'GET':
        # implement elastic search
        search_text_query = request.GET['esearch']
        crop = Crop.objects.filter(crop_level__icontains=search_text_query)
        kaggle_crop_detail = kagel_crop.objects.filter(crop_name__icontains=search_text_query)


    # paginator
    paginator = Paginator(crop, 6)
    kaggle = Paginator(kaggle_crop_detail, 6)


    page_number = request.GET.get('page')
    crops = paginator.get_page(page_number)

    page_number = request.GET.get('page')
    kaggle_crop_detail = kaggle.get_page(page_number)

    # Calculate the page range
    page_range = paginator.page_range
    current_page = crops.number
    total_pages = paginator.num_pages

    # Determine which pages to display
    start_page = max(current_page - 4, 1)
    end_page = min(current_page + 4, total_pages)

    if end_page - start_page < 9:
        if start_page > 1:
            end_page = min(start_page + 9, total_pages)
        else:
            start_page = max(end_page - 9, 1)

    page_range_to_show = list(range(start_page, end_page + 1))

    context = {
        'crops': crops,
        'kaggle_crops': kaggle_crop_detail,
        'page_range_to_show': page_range_to_show,
        'has_previous': crops.has_previous(),
        'has_next': crops.has_next(),
        'previous_page_number': crops.previous_page_number() if crops.has_previous() else None,
        'next_page_number': crops.next_page_number() if crops.has_next() else None,
        # Add other context variables as needed
    }


    return render(request, 'search.html',context)
