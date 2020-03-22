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
	info['message'] = 'This is the API to consume blog posts'
	info['services'] = []
	info['services'].append({'url': '/api/posts', 'method': 'GET', 'description': 'Gets a list of posts'})
	print(info)
	return jsonify(info)


# Show all users
@app.route('/api/users', methods=['GET'])
def get_users():
	users = User.query.all()
	return jsonify(users)


# Show all posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
	posts = Picture.query.all()
	return jsonify(posts)


# Show a picture
@app.route('/api/picture/<int:picture_id>', methods=['GET'])
def get_post(post_id):
	post = db.session.query(Picture).get(post_id)
	if post:
		return jsonify(post), 200
	else:
		return abort(404) # 404 is not found


# Create picture
@app.route('/api/posts', methods=['POST'])
def create_post():
	data = request.json
	if 'title' in data and 'content_type' in data and 'content' in data and 'user' in data:
		post = Picture(title=data['title'],
					   content_type=data['content_type'],
					   content=data['content'],
					   user_id=int(data['user']))
		db.session.add(post)
		try:
			db.session.commit() # how would you improve this code?
			return jsonify(post), 201 # status 201 means "CREATED"
		except:
			db.session.rollback()
			abort(400)
	else:
		return abort(400) # 400 is bad request


# Replace picture
@app.route('/api/picture/<int:picture_id>', methods=['PUT'])
def replace_post(post_id):
	post = db.session.query(Picture).get(post_id)
	if post:
		data = request.json
		if 'title' in data and 'content_type' in data and 'content' in data and 'user' in data:
			post.title = data['title']
			post.content_type = data['content_type']
			post.content = data['content']
			post.user_id = data['user']
			try:
				db.session.commit()
				return jsonify(post), 200
			except:
				db.sesion.rollback()
				abort(400)
		else:
			return abort(400) # bad request
	else:
		return abort(404)  # 404 is not found
