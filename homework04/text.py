import pandas as pd
import requests
import textwrap
import config
import pymorphy2
import emoji



from pandas.io.json import json_normalize
from string import Template
from tqdm import tqdm
from nltk.corpus import stopwords

stopwords = stopwords.words("russian")

def get_wall(
    owner_id: str='',
    domain: str='',
    offset: int=0,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103',
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """
    code = ("return API.wall.get({" +
        f"'owner_id': '{owner_id}'," +
        f"'domain': '{domain}'," +
        f"'offset': '{offset}'," +
        f"'count': '{count}'," +
        f"'filter': '{filter}'," +
        f"'extended': '{extended}'," +
        f"'fields': '{fields}'," +
        f"'v': '{v}'" +
    "});")

    response = requests.post(
        url="https://api.vk.com/method/execute",
            data={
                "code": code,
                "access_token": config.VK_CONFIG["access_token"],
                "v": "5.103"
            }
    )

    response = response.json()

    texts = []

    for i in range (len(response['response']['items'])):
        texts += [[response['response']['items'][i]['text']]]

    return texts


def del_links(text):
    text = text.split()
    for i in range(len(text)):
        if 'http' in text[i] or 'vk' in text[i]:
            text[i] = ''
    return ' '.join(text)
def del_stopwords(text):
    text = text.split()
    for i in range(len(text)):
        if text[i] in stopwords:
            text[i] = ''
    return ' '.join(text)

def clean(texts):
    forbidden=('…','–','`','~','!','@','#','№','$','\\','«','»',';','%','^',':','&','?','*','(',')','_','–','+','=','{','}','[',']','|',';','\'','\"','<','>',',','.','?','/', '-', '\n')
    for i in range (len(texts)):
        texts[i][0] = del_links(texts[i][0])
        texts[i][0] = "".join([symbol for symbol in texts[i][0] if not symbol in forbidden])
        texts[i][0] = ''.join(c for c in texts[i][0] if not c in emoji.UNICODE_EMOJI)
        texts[i][0] = del_stopwords(texts[i][0])

    return texts

def normalize(domain):
    texts = get_wall(domain=domain)
    texts = clean(texts)
    morph = pymorphy2.MorphAnalyzer()
    for i in range (len(texts)):
        text = texts[i][0].split()
        for j in range (len(text)):
            p = morph.parse(text[j])[0]  # Делаем полный разбор, и берем первый вариант разбора (условно "самый вероятный", но не факт что правильный)
            text[j] = p.normal_form
        texts[i][0] = ' '.join(text)
    return texts
