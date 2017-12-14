
import logging
from app.tasks import process_image, get_s3_bucket
from models import Image

logger = logging.getLogger()


class Main(object):

    def __init__(self):
        logging.basicConfig(level=logging.INFO)

        # create a file handler
        handler = logging.FileHandler('server.log')
        handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter(
            '[%(asctime)s: %(levelname)s/%(name)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def load_images(self, bucket_name=None):
        bucket = get_s3_bucket(bucket_name)
        if bucket:
            for key in bucket.objects.all():
                if not key.key.endswith(".tar.gz") and\
                        not key.key.endswith("undefined.jpg"):

                    image = Image(name=key.key, size=key.size)
                    image.save()
                    process_image.delay(image.id, image.name)
