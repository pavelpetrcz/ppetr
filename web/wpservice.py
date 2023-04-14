import os
import requests as re

bearer_jwt = os.getenv('B_JWT')
headers = {"Authorization": bearer_jwt}
base_url = 'https://192-168-88-141.nomakcz.direct.quickconnect.to/wordpress'


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


def get_img_url(img_id):
    """
    Get URL of the image
    @param img_id: id of media asset in string
    """
    url_to_requst = base_url + "/index.php/wp-json/wp/v2/media/" + img_id
    response = re.get(url_to_requst, headers=headers)
    return response
