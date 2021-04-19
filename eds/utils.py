import secrets
import random
import os
from PIL import Image
from eds import app
from datetime import datetime as dt
from datetime import timedelta
import base64
from flask_login import current_user

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/assets/images', picture_fn)
	
	i = Image.open(form_picture)
	i.save(picture_path)
	
	with open(picture_path, "rb") as imageFile:
		encoded_string = base64.b64encode(imageFile.read())

	return encoded_string

#work on this
def decode_picture(image):
	image = image.replace('\\','',1)
	image_encode = image.encode('utf-8')
	image_decode = base64.decodebytes(image_encode)
	return image_decode

def delete_picture(pic_name):
	picture_path = os.path.join(app.root_path, 'static/assets/images', pic_name)
	os.remove(picture_path)
