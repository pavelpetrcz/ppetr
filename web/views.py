import os

from butter_cms import ButterCMS
from django.shortcuts import render


def home(request):
    return render(request, 'web/index.html')


def blog(request):
    return render(request, 'web/blog.html')


def blogpost(request):
    if request.method == 'GET':
        api_key = os.getenv('BUTTER')
        client = ButterCMS(api_key)
        sample_page = client.pages.get('*', 'simple-page')

        context = {'beers_list': sample_page}
        return render(request, 'web/blogpost.html', context)
