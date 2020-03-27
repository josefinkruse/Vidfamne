import os
from flaskblog import db, bcrypt
from flaskblog.models import User, Folder, Picture, Comment
from datetime import datetime, date

# create new trip
# os.mkdir("flaskblog/static/<int:folder_title>")
# os.mkdir("flaskblog/static/trip_2")

try:
    os.remove('flaskblog/site.db')
    print('previous DB file removed')
except:
    print('no previous file found')

db.create_all()

hashed_password = bcrypt.generate_password_hash('testing').decode('utf-8')
default_user = User(username='Default user', email='default@test.com', password=hashed_password)
db.session.add(default_user)

first_folder = Folder(title='First folder', start_date=date.fromisoformat('2019-07-11'), end_date=date.fromisoformat('2019-07-18'),
                      destinations='Marstrand', description='Best trip ever!', folder_image='trip_1.1.jpg')
db.session.add(first_folder)

second_folder = Folder(title='Second folder', start_date=date.fromisoformat('2019-08-11'), end_date=date.fromisoformat('2019-08-18'),
                       destinations='Vinga', description='Second best trip ever!', folder_image='trip_2.1.jpg')
db.session.add(second_folder)

for i in range(11):
    picture = Picture(description='Image description', date_taken=datetime.utcnow(), image_file=f'trip_1.{i+1}.jpg',
                  user=default_user, folder=first_folder)
    db.session.add(picture)

for i in range(5):
    picture = Picture(description='Image description', date_taken=datetime.utcnow(), image_file=f'trip_2.{i+1}.jpg',
                  user=default_user, folder=second_folder)
    db.session.add(picture)

'''
picture2 = Picture(description='First', date_taken=datetime.utcnow(), image_file='IMG_3886.JPG',
                  user=default_user, folder=second_folder)
db.session.add(picture2)

picture3 = Picture(description='First', date_taken=datetime.utcnow(), image_file='IMG_20170703_145342.jpg',
                  user=default_user, folder=second_folder)
db.session.add(picture3)

picture4 = Picture(description='First', date_taken=datetime.utcnow(), image_file='IMG_20170703_212027.jpg',
                  user=default_user, folder=second_folder)
db.session.add(picture4)

comment = Comment(user=default_user, content='Lorem ipsum dolor sit amet, consectetuer adipiscing elit. ',
                  picture=picture1)
# ---- picture=picture?

db.session.add(comment)
'''
db.session.commit()

print('finalized')
folders=Folder.query.all()
print(folders)