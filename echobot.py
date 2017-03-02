import json
import requests
import redis
import sys

BOT_TOKEN = sys.argv[1]
BOT_URL = 'https://api.telegram.org/bot{}/'.format(BOT_TOKEN)
BOT_SEND_MESSAGE_URL = BOT_URL+'sendMessage?chat_id={}&text={}'
BOT_MESSAGES_OFFSET = 'offset'
POOLING_TIMEOUT = 100  # seconds
BOT_RECEIVED_MESSAGES_URL = BOT_URL+'getUpdates?timeout={}'.format(
                                                            POOLING_TIMEOUT)
# BOT_RECEIVED_MESSAGES_URL = BOT_URL+'getUpdates'

cache = redis.StrictRedis(host='localhost', port=32768, db=0)


def make_bot_request(url):
    resp = requests.get(url)
    content = resp.content.decode('utf-8')
    return content


def json_to_python_from_url(url):
    content = make_bot_request(url)
    python_obj = json.loads(content)
    return python_obj


def get_updates():
    print('Checking updates')
    python_obj = json_to_python_from_url(
        BOT_RECEIVED_MESSAGES_URL+'&offset={}'.format(
            int(cache.get(BOT_MESSAGES_OFFSET))))
    return python_obj


def get_messages(updates):
    chat_update_id = []
    for m in updates['result']:
        chat_id = m['message']['chat']['id']
        chat_message = m['message']['text']
        chat_update_id.append(m['update_id'])
        cache.set(BOT_MESSAGES_OFFSET, max(chat_update_id)+1)
        # message id whe´re expecting to receive
        yield chat_id, chat_message


def send_message(chat_id, text_to_send):
    url = BOT_SEND_MESSAGE_URL.format(chat_id, chat_message)
    print('Sending message to {}'.format(chat_id))
    make_bot_request(url)


if __name__ == '__main__':
    while True:
        print('offset@main {}'.format(int(cache.get(BOT_MESSAGES_OFFSET))))
        for chat_id, chat_message in get_messages(get_updates()):
            send_message(chat_id, chat_message)
