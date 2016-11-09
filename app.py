from boto.exception import S3ResponseError
from boto.s3.key import Key
import boto
from tasks import process_image
import sys

def load_images(bucket_name):
	try:
		bucket_name = bucket_name or "waldo-recruiting"
		conn = boto.connect_s3()
		bucket = conn.get_bucket(bucket_name)

		for key in bucket.list():
			process_image.delay(key)
	except S3ResponseError, e:
            print "We should have public-read access, but received an error: %s" % e
            
if __name__ == '__main__':
	bn = None
	if len(sys.argv) > 1:
		bn = sys.argv[1]
	load_images(bn)



