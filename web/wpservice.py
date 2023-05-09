import os
import requests as re

bearer_jwt = os.getenv('B_JWT')
headers = {"Authorization": bearer_jwt}
base_url = os.getenv('BASE_URL')


# TODO: error handling
def get_all_post():
    """
    Get all posts
    @return: Response object from WP
    """
    response = re.get(base_url + '/wp-json/wp/v2/posts',
                      headers=headers
                      )
    return response


def get_post(post_id):
    """
    Retrieve specific post according to id
    @param post_id: numeric od of post
    @return: Response of REST API
    """
    response = re.get(base_url + '/wp-json/wp/v2/posts/' + post_id, headers=headers)
    return response


def get_all_images():
    """
    Get all media assets in one call
    @return: all media assets
    """
    url_to_request = base_url + "/wp-json/wp/v2/media"
    response = re.get(url_to_request, headers=headers)
    return response
