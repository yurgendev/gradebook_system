from django.core.paginator import Paginator
from django.shortcuts import render
from .models import News


def news_list(request):
    news_page_list = News.objects.all()
    paginator = Paginator(news_page_list, 5)  # Show 5 news per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {'page_obj': page_obj})

