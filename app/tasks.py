import cStringIO
import json
import logging
import boto3
import botocore
from tqdm import tqdm
from botocore.handlers import disable_signing
from celery import Celery
from config import CELERY_BROKER, DEFAULT_BUCKET
from models import dal, Image
from PIL import Image as PILImage

logger = logging.getLogger()
app = Celery('tasks', broker=CELERY_BROKER)


@app.task
def process_image(id, name):
    filename = name

    logger.info("Downloading File: %s" % filename)

    try:
        obj = s3.Object(DEFAULT_BUCKET, name)
        total_size = float(obj.get()['ContentLength'])
        pbar = tqdm(total=total_size, unit='B',
                    unit_scale=True, unit_divisor=1024)

        def progress(bytes_amount):
            pbar.update(bytes_amount)

        img = cStringIO.StringIO()
        obj.download_fileobj(img, Callback=progress)
        pbar.close()
        logger.info('Download Complete. File: {}. Total Size: {}.'.format(
            filename, str(total_size)))

        exif = json.dumps(read_exif(img), encoding='latin1')

        logger.info("Extracted exif. Now saving to DB. File: %s" % filename)

        image = dal.session.query(Image).get(id)
        image.update(exif_info=exif)

    except Exception as e:
        logger.exception(e)


def read_exif(file):
    img = PILImage.open(file)
    exif_data = img._getexif()
    return exif_data


def get_s3_bucket(bucket_name):
    s3 = get_s3_connection()
    bucket_name = bucket_name or DEFAULT_BUCKET
    bucket = False
    try:
        bucket = s3.Bucket(bucket_name)
    except botocore.exceptions.ClientError as e:
        logger.exception(e)
    return bucket


def get_s3_connection():
    s3 = boto3.resource('s3')
    s3.meta.client.meta.events.register(
        'choose-signer.s3.*', disable_signing)
    return s3


s3 = get_s3_connection()
