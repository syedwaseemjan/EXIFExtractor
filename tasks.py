from celery import Celery
from config import CELERY_BROKER
import PIL.Image
import cStringIO
import json
import collections
import sqlite3
from models import session, Image
from sqlalchemy.exc import IntegrityError

app = Celery('tasks', broker=CELERY_BROKER)

@app.task
def process_image(key):
	filename = key.name.encode('utf-8')
	
	print "Downloading: %s" % filename
	
	try:
		img = cStringIO.StringIO(key.get_contents_as_string())
		exif = (json.dumps(convert(read_exif(img)), ensure_ascii=False))

		print "Extracted exif. Now saving to DB. File: %s" % filename
		
		image = Image(name=filename, \
					size=key.size, \
					exif_info=sqlite3.Binary(exif))

		session.add(image)

		try:
			session.commit()
			print "Successfully saved to DB: %s" % filename
		except IntegrityError, exc:
			session.rollback()
			print 'error', exc.message
			
	except Exception as e:
		print e
	

def convert(data):
	if isinstance(data, basestring):
		return str(data)
	elif isinstance(data, collections.Mapping):
		return dict(map(convert, data.iteritems()))
	elif isinstance(data, collections.Iterable):
		return type(data)(map(convert, data))
	else:
		return data

def read_exif(file):
	img = PIL.Image.open(file)
	exif_data = img._getexif()
	return exif_data