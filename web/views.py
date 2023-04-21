import json
import sys
import traceback

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
    sys.stderr.write('views.blog started to process\n')
    if request.method == 'GET':
        list_of_blogposts = []

        # load all posts
        try:
            response = wp.get_all_post()
            all_posts = json.loads(response.text)
            sys.stderr.write('path /blog - all done' + all_posts)
        except Http404:
            msg = 'Unable to load blogposts.'
            sys.stderr.write(msg)
            raise Http404(msg)
        except TimeoutError:
            msg = 'Requst timed out.'
            sys.stderr.write(msg)
            raise TimeoutError(msg)
        except Exception:
            msg = 'Exception'
            sys.stderr.write(msg + str(traceback.extract_stack()))

        # iterate all posts
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
            sys.stderr.write('Iteration through posts failed.')
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
