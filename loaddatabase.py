import os
from flaskblog import db, bcrypt
from flaskblog.models import User, Folder, Picture, Comment
from datetime import datetime, date
import shutil

try:
    os.remove('flaskblog/site.db')
    print('previous DB file removed')
except:
    print('no previous file found')

for i in range(20):
    try:
        shutil.rmtree(f'flaskblog/static/trip_{i + 3}')
        print(f'directory: trip_{i + 3} removed')
    except FileNotFoundError:
        pass
    else:
        pass

db.create_all()

hashed_password = bcrypt.generate_password_hash('testing').decode('utf-8')
default_user = User(username='Default user', email='default@test.com', password=hashed_password)
db.session.add(default_user)

user_1 = User(username='User 1', email='user_1@test.com', password=hashed_password)
db.session.add(user_1)

first_folder = Folder(title='Sailing week 2019', start_date=date.fromisoformat('2019-07-13'), end_date=date.fromisoformat('2019-07-21'),
                      destinations='Marstrand, Hönö, Björkö', description='Amazing trip!', folder_image='trip_1.1.jpg')
db.session.add(first_folder)

second_folder = Folder(title='Weekend september 2019', start_date=date.fromisoformat('2019-09-11'), end_date=date.fromisoformat('2019-09-13'),
                       destinations='Vinga, Styrsö, Känsö', description='Best trip ever!', folder_image='trip_2.1.jpg')
db.session.add(second_folder)

for i in range(11):
    picture = Picture(description='Image description', date_taken=datetime.utcnow(), image_file=f'trip_1.{i+1}.jpg',
                  user=default_user, folder=first_folder)
    db.session.add(picture)

for i in range(5):
    picture = Picture(description='Image description', date_taken=datetime.utcnow(), image_file=f'trip_2.{i+1}.jpg',
                  user=user_1, folder=second_folder)
    db.session.add(picture)

comment = Comment(user=user_1, content='Great picture!', picture_id=1)
db.session.add(comment)

comment = Comment(user=default_user, content='Beautiful!', picture_id=11)
db.session.add(comment)

comment = Comment(user=default_user, content='Great memory!', picture_id=16)
db.session.add(comment)

db.session.commit()

print('finalized')
folders=Folder.query.all()
print(folders)