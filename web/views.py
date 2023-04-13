import json
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render

from ppetr import settings
from web import wpservice as wp


def home(request):
    return render(request, 'web/index.html')
    # TODO: refactor to objects in django templates https://docs.djangoproject.com/en/4.1/ref/templates/language/


def blog(request):
    if request.method == 'GET':
        list_of_blogposts = []

        # load all posts
        try:
            response = wp.get_all_post()
            all_posts = json.loads(response.text)
        except Http404:
            raise Http404("Unable to load blogposts.")
        except TimeoutError:
            raise TimeoutError("Requst timed out.")
        try:
            for post in all_posts:
                img = post["featured_media"]

                if img == 0:
                    i = settings.DEFAULT_BLOGPOST_IMG
                else:
                    image_url = json.loads(wp.get_img_url(str(img)).text)
                    i = image_url["guid"]["rendered"]

                b = {
                    "body": post["content"]["rendered"],
                    "title": post["title"]["rendered"],
                    "summary": post["excerpt"]["rendered"],
                    "image_url": i,
                    "post_id": post["id"],
                    "publishedAt": convert_dt_to_str(post["date"])
                }
                list_of_blogposts.append(b)
        except TypeError or ValueError or RuntimeError or KeyError:
            raise Exception('Unexpected error. Try again later.')
        # TODO: logging or errors https://sentry.io/welcome/

        context = {'posts_list': list_of_blogposts}
        return render(request, 'web/blog.html', context)
    else:
        raise Http404("Incorrect HTTP method.")


def blogpost(request, post_id):
    if request.method == 'GET':
        try:
            post = wp.get_post(post_id)
            j_post = json.loads(post.text)
            post = {
                "title": j_post["title"]["rendered"],
                "body": j_post["content"]["rendered"]
            }
            context = {'blogpost': post}
        except NameError or ObjectDoesNotExist:
            raise Http404('Blogpost does not exists.')
        return render(request, 'web/blogpost.html', context)
    else:
        raise Http404('Incorrect HTTP method.')


def convert_dt_to_str(dt):
    """
    Convert date time format
    :param dt: string %Y-%m-%dT%H:%M:%S.%f%Z
    :return: string %d.%m.%Y
    """
    d = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
    return datetime.strftime(d, '%d.%m.%Y')
