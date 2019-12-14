import requests
import time

import config


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = MinDelay
    retrise=0
    while True:
        try:
            if max_retries-retrise==0 and retrise!=0:
                return None
            quest=requests.get(url=url,params=params,timeout=timeout)
            quest.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(e)
            print(delay)
        except requests.exceptions.ReadTimeout as e:
            print(e)
            print(delay)
        except requests.exceptions.ConnectTimeout as e:
            print(e)
            print(delay)
        else:
            return quest.json()
        finally:
            retrise+=1
            time.sleep(delay)
            delay = min(delay * Factor, timeout)
            delay = delay + random.normalvariate(delay,backoff_factor)



def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"


    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}".format(
            domain = config.VK_CONFIG['domain'],
            access_token = config.VK_CONFIG['access_token'],
            user_id = user_id,
            fields = fields,
            v = config.VK_CONFIG['version'])

    response = requests.get(query)

    return response.json()

def messages_get_history(user_id, offset=0, count=20):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE
