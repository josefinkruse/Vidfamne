# This file is meant to test the functionalities of the API built in this software.
# Official documentation: https://requests.readthedocs.io/en/master/
from datetime import datetime

import requests
import json
from flask import url_for

# definitions of host and port
host = 'localhost'
port = 5000

fail = False # keeps track if any of the tests had failed

# step 1: get the token
reply = requests.get(f'http://{host}:{port}/api/token/public')
if reply.status_code == 200:
    print('request successful')
    token = reply.text
    print('My authentication token is:', token)
else:
    print('request was not successful')
    fail = True
token_dict = json.loads(token)

# step 2: getting information about the web service
req_headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token_dict["token"]}'
               }
reply = requests.get(f'http://{host}:{port}/api/', headers=req_headers)

print('Status:', reply.status_code)

if reply.status_code == 200:
    print(reply.json())
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True

# step 3: getting a list of pictures
reply = requests.get(f'http://{host}:{port}/api/pictures', headers=req_headers)

print('Code:', reply.status_code)

if reply.status_code == 200:
    for picture in reply.json():
        print('Picture', picture['id'])
        for key, value in picture.items():
            if key == 'content':
                print('\t', key.ljust(15), ':', value[:50].replace('\n', ''), '...')
            elif key == 'id':
                continue
            elif isinstance(value, dict):
                print('\t', key, ':')
                for k2, v2 in value.items():
                    print('\t\t', k2.ljust(15), ':', v2)
            else:
                print('\t', key.ljust(15), ':', value)
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True

# step 4: inserting a new picture
picture = {'image_file': "flaskblog/static/trip_1/trip_1.12.jpg",
       'date_taken': datetime.utcnow().strftime("%Y-%m-%d"),
       'description': 'Description',
       'place_taken': 'Vinga',
       'user': 2,
       'folder': 2}

reply = requests.post(f'http://{host}:{port}/api/pictures', headers=req_headers, data=json.dumps(picture))

if reply.status_code == 201:
    print('Created with success')
    picture_received = reply.json()
    print('Picture created:')
    print('\tid:', picture_received['id'])
    print('\tdescription:', picture_received['description']) # ------------
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True
else:
    print('There was an error:', reply.status_code)
    fail = True


# step 5: getting a specific picture
reply = requests.get(f'http://{host}:{port}/api/picture/1', headers=req_headers)

if reply.status_code == 200:
    print('Picture found:')
    for key, value in reply.json().items():
        print('\t', key, ':', value)
elif reply.status_code == 404:
    print('Picture not found! Try another id!')
    fail = True
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True

# step 6: replacing a picture
picture = {'image_file': "flaskblog/static/trip_1/trip_1.13.jpg",
       'date_taken': datetime.utcnow().strftime("%Y-%m-%d"),
       'description': 'Description',
       'place_taken': 'Vinga',
       'user': 2,
       'folder': 2}

reply = requests.put(f'http://{host}:{port}/api/picture/17', headers=req_headers, data=json.dumps(picture))

if reply.status_code == 200:
    print('Replaced with success')
    picture_received = reply.json()
    print('Picture created:')
    print('\tid:', picture_received['id'])
    print('\tdescription:', picture_received['description'])
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True
else:
    print('There was an error:', reply.status_code)
    print(reply.text)
    fail = True

# step 7: editing a picture
picture = {'image_file': "flaskblog/static/trip_1/trip_1.12.jpg",
#       'date_taken': datetime.utcnow(),
#       'description': 'Description',
#       'place_taken': 'Vinga',
#       'user': 2,
#       'folder': 2
        }

reply = requests.put(f'http://{host}:{port}/api/picture/17', headers=req_headers, data=json.dumps(picture))

if reply.status_code == 200:
    print('Updated with success')
    picture_received = reply.json()
    print('Picture created:')
    print('\tid:', picture_received['id'])
    print('\tdescription:', picture_received['description'])
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True
else:
    print('There was an error:', reply.status_code)
    print(reply.text)
    fail = True

# step 8: deleting a picture
reply = requests.delete(f'http://{host}:{port}/api/picture/17/delete', headers=req_headers)

if reply.status_code == 200:
    print('Picture deleted:')
    for key, value in reply.json().items():
        print('\t', key, ':', value)
elif reply.status_code == 404:
    print('Picture not found! Try another id!')
    fail = True
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True
else:
    print('Unknown error:', reply.status_code)
    fail = True
    print(reply.text)


if not fail:
    print('THE TESTS WERE SUCCESSFUL')
else:
    print('THE TESTS WERE NOT SUCCESSFUL')