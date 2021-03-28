import secrets
import random
import os
from eds import app
from datetime import datetime as dt
from datetime import timedelta
from flask_login import current_user

def unique_id(x=7):
    token = secrets.token_hex(16)[:x]
    new_token = ' '.join(token).split(' ')
    main_id = ''.join(random.sample(new_token, len(new_token)-1))
    return (main_id)

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/assets/images/screenshots', picture_fn)
	
	i = Image.open(form_picture)
	i = resizeimage.resize_cover(i, [213, 150], validate=False)
	i.save(picture_path)
	
	return picture_fn

def delete_picture(pic_name):
	picture_path = os.path.join(app.root_path, 'static/assets/images', pic_name)
	os.remove(picture_path)

#returns the current date
def date_stuff():
	date = dt.now()
	post_date = date.strftime('%Y-%b-%d %H:%M')
	return post_date
