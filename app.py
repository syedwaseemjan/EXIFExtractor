from boto.exception import S3ResponseError
from boto.s3.key import Key
import boto
from tasks import process_image

def load_images():
	conn = boto.connect_s3()
	bucket = conn.get_bucket("waldo-recruiting")

	try:
		for key in bucket.list():
			process_image.delay(key)
	except S3ResponseError, e:
            self.fail("We should have public-read access, but received "
                      "an error: %s" % e)
            
if __name__ == '__main__':
	load_images()




