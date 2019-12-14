import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends = get_friends(user_id,'bdate')
    months = []

    for i in range (friends['response']['count']):
        try:
            date = list(map(int, friends['response']['items'][i]['bdate'].split('.')))

            months += [date[1] + date[2]*12]
        except:
            pass

    date = dt.datetime.now()
    count_months = date.year * 12 + date.month

    return (count_months - median(months)) // 12
