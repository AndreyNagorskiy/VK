import requests
import csv
from datetime import datetime
from time import sleep


def main():
    start = datetime.now()
    group_id = 'group_id'  # Change
    offset = 0
    date_x = 1493596800  # Unix time
    all_posts = []
    token = 'token'  # Change

    while True:
        sleep(1)
        r = requests.get('https://api.vk.com/method/wall.get',
                         params={'owner_id': group_id,
                                 'count': 100,
                                 'offset': offset,
                                 'access_token': token,
                                 'v': '5.95'})
        posts = r.json()['response']['items']
        all_posts.extend(posts)
        oldest_post_date = posts[-1]['date']
        offset += 100
        print(offset)
        if oldest_post_date < date_x:
            break

    for post in all_posts:
        post_data = get_data(post)
        write_csv(post_data)

    end = datetime.now()
    total = end - start
    print(len(all_posts))
    print(str(total))


def write_csv(data):
    with open('posts_data.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((data['likes'],
                         data['reposts'],
                         data['text']
                         ))


def get_data(post):
    try:
        post_id = post['id']
    except:
        post_id = 0
    try:
        likes = post['likes']['count']
    except:
        likes = 'zero'
    try:
        reposts = post['reposts']['count']
    except:
        reposts = 'zero'
    try:
        text = post['text']
    except:
        text = '***'
    data = {'id': post_id, 'likes': likes, 'reposts': reposts, 'text': text}
    return data
