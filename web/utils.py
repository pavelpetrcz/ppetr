from datetime import datetime
from ppetr import settings


def get_image_url(media, img):
    """
    get url of image according to id of image
    @param media: list of medias from /wp-json/wp/v2/media
    @param img: id of featured image
    @return: URL of image
    """
    for item in media:
        if item["id"] == img:
            url = item["guid"]["rendered"]
            return url
        elif item["id"] != img:
            continue
        else:
            return settings.DEFAULT_BLOGPOST_IMG


def convert_dt_to_str(dt):
    """
    Convert date time format
    :param dt: string %Y-%m-%dT%H:%M:%S.%f%Z
    :return: string %d.%m.%Y
    """
    d = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
    return datetime.strftime(d, '%d.%m.%Y')
