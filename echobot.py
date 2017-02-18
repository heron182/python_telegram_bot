import json, requests

BOT_TOKEN = ''
BOT_URL = 'https://api.telegram.org/bot{}/'.format(BOT_TOKEN)
BOT_RECEIVED_MESSAGES_URL = BOT_URL+'getUpdates'
BOT_SEND_MESSAGE_URL = BOT_URL+'sendMessage?chat_id={}&text={}'

def get_url(url):
    resp = requests.get(url)
    content = resp.content.decode('utf-8')
    return content

def json_to_python_from_url(url):
    content = get_url(url)
    python_obj = json.loads(content)
    return python_obj

def get_updates():
    python_obj = json_to_python_from_url(BOT_RECEIVED_MESSAGES_URL)
    return python_obj

def get_last_chat_id_and_text(updates):
    num_updates = len(updates['result'])
    last_update = num_updates - 1
    chat_id = updates['result'][last_update]['message']['chat']['id']
    chat_message = updates['result'][last_update]['message']['text']
    return (chat_id, chat_message)

def send_message(chat_id, text_to_send):
    url = BOT_SEND_MESSAGE_URL.format(chat_id, chat_message)
    get_url(url)

if __name__ == '__main__':
    last_chat = (None, None)
    while True:
        chat_id, chat_message = get_last_chat_id_and_text(get_updates())
        if (chat_id, chat_message) != last_chat:
            send_message(chat_id, chat_message)
        last_chat = chat_id, chat_message
