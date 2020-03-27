from flask import request, jsonify, abort, make_response, Response
from flaskblog import app, db, bcrypt
from flaskblog.models import Token, Picture, User
import datetime


# method used to create a token that can be used for some time defined by the delta
@app.route('/api/token/public', methods=['GET'])
def token():
	expired = datetime.datetime.now() + datetime.timedelta(minutes=60)
	token_string = bcrypt.generate_password_hash(str(expired)).decode('utf-8')
	new_token = Token(token=token_string, date_expired=expired)
	db.session.add(new_token)
	try:
		db.session.commit()
		return jsonify({'token': token_string, 'expire': expired.strftime('%Y-%m-%d %H:%M:%S')})
	except:
		db.session.rollback()
		return abort(400)


# method used to inform the user of the webservice regarding its capabilities
@app.route('/api/', methods=['GET'])
def api():
	info = dict()
	info['message'] = 'This is the API to consume blog pictures'
	info['services'] = []
	info['services'].append({'url': '/api/pictures', 'method': 'GET', 'description': 'Gets a list of pictures'})
	print(info)
	return jsonify(info)


# Show all users
@app.route('/api/users', methods=['GET'])
def get_users():
	users = User.query.all()
	return jsonify(users)


# Show all pictures
@app.route('/api/pictures', methods=['GET'])
def get_pictures():
	pictures = Picture.query.all()
	return jsonify(pictures)


# Show a picture
@app.route('/api/picture/<int:picture_id>', methods=['GET'])
def get_picture(picture_id):
	picture = db.session.query(Picture).get(picture_id)
	if picture:
		return jsonify(picture), 200
	else:
		return abort(404) # 404 is not found


# Create picture
@app.route('/api/pictures', methods=['POST'])
def create_picture():
	data = request.json
	if 'image_file' in data and 'date_taken' in data and 'description' in data and 'place_taken' in data and 'user' in data and 'folder' in data:
		picture = Picture(image_file=data['image_file'],
					   date_taken=datetime.datetime.strptime(data['date_taken'], "%Y-%m-%d"),
					   description=data['description'],
					   place_taken=data['place_taken'],
					   user_id=int(data['user']),
						folder_id= int(data['folder']))

		db.session.add(picture)

		try:
			db.session.commit() # how would you improve this code?
			return jsonify(picture), 201 # status 201 means "CREATED"
		except Exception as e:
			db.session.rollback()
			abort(400)
	else:
		return abort(400) # 400 is bad request


# Replace picture
@app.route('/api/picture/<int:picture_id>', methods=['PUT'])
def replace_picture(picture_id):
	picture = db.session.query(Picture).get(picture_id)
	if picture:
		data = request.json
		if 'image_file' in data:
			picture.image_file = data['image_file']
		if 'date_taken' in data:
			picture.date_taken = datetime.datetime.strptime(data['date_taken'], "%Y-%m-%d")
		if 'description' in data:
			picture.description = data['description']
		if 'place_taken' in data:
			picture.place_taken= data['place_taken']
		if 'user' in data:
			picture.user_id = data['user']
		if 'folder' in data:
			picture.folder_id = data['folder']
		try:
			db.session.commit()
			return jsonify(picture), 200
		except Exception as e:
			db.session.rollback()
			abort(400)
	else:
		return abort(404)  # 404 is not found


# Delete a picture
@app.route("/api/picture/<int:picture_id>/delete", methods=['DELETE'])
def delete_picture_api(picture_id):
	picture = Picture.query.get_or_404(picture_id)
	db.session.delete(picture)
	# Cant remove pictures with comments. Check if picture has comment, remove them first, and then remove picture
	try:
		db.session.commit()
		return jsonify(picture), 200
	except Exception as e:
		db.session.rollback()
		abort(400)

