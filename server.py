from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import random
import instagrapi

app = Flask(__name__)
CORS(app)

@app.route('/api/send-dms', methods=['POST'])
def send_dms():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    message = data.get('message')
    hashtags = data.get('hashtags')

    cl = Connect(username, password)
    Interact(cl, message, hashtags)

    return jsonify({'result': 'Direct messages sent successfully'})

def Connect(username, password):
    ''' Log onto Instagram '''
    cl = instagrapi.Client()
    if os.path.exists(f'{username}.json'):
        cl.load_settings(f'{username}.json')
        cl.login(username, password)
    else:
        cl.login(username, password)
        cl.dump_settings(f'{username}.json')
    ID = cl.user_id
    cl.delay_range = [5, 10]
    cl.get_timeline_feed()
    print(f'[+] Login successful')
    return cl

def Interact(cl, message_text, hashtags):
    n_posts = random.randint(5, 10)
    posts = cl.hashtag_medias_recent_v1(hashtags, n_posts)
    TarIDs = [post.user.pk for post in posts]

    for u in TarIDs:
        cl.direct_send(message_text, user_ids=[u])
        cl.delay_range = [10, 30]

    print(f'[+] Direct messaged {n_posts} users')
    cl.delay_range = [10, 30]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
