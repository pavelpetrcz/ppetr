from datetime import datetime
import os

from butter_cms import ButterCMS
from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

api_key = os.getenv('BUTTER')
client = ButterCMS(api_key)


def home(request):
    return render(request, 'web/index.html')
    # TODO: refactor to objects in django templates https://docs.djangoproject.com/en/4.1/ref/templates/language/


def contact(request):
    return render(request, 'web/contact.html')


def blog(request):
    if request.method == 'GET':
        all_posts = client.posts.all()
        list_of_blogposts = []
        for post in all_posts['data']:
            b = {
                "body": post["body"],
                "title": post["title"],
                "summary": post["summary"],
                "image_url": post["featured_image"],
                "slug": post["slug"]
                # "publishedAt": convert_dt_to_str(post["published"]) FIXME: show converted date of blogpost
            }
            list_of_blogposts.append(b)
        context = {'posts_list': list_of_blogposts}
        return render(request, 'web/blog.html', context)


def blogpost(request, slug):
    if request.method == 'GET':
        try:
            selected_post = client.posts.get(slug=slug)
            post = {
                "title": selected_post["data"]["title"],
                "body": selected_post["data"]["body"]
            }
            context = {'blogpost': post}
        except NameError or ObjectDoesNotExist:
            raise Http404('Blogpost does not exists.')
        return render(request, 'web/blogpost.html', context)


def convert_dt_to_str(dt):
    """
    Convert date time format
    :param dt: string %Y-%m-%dT%H:%M:%S.%f%Z
    :return: string %d.%m.%Y
    """
    d = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%f%Z')
    return datetime.strftime(d, '%d.%m.%Y')
