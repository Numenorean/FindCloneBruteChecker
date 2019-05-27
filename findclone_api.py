import requests

l_url = 'https://findclone.ru/login'


def check(phone, password, proxies=None):
    l = requests.post(l_url, data={'phone':phone, 'password':password}, proxies=proxies).json()
    if 'Error' in list(l.keys()):
        return None
    else:
        period = int(round(l['Period'] / 86400, 0))
        quantity = l['Quantity']
        typename = l['TypeName']
        return '''
Данные для входа - {}:{}
Период: осталось {} дней
Осталось запросов: {}
Тариф: {}
---------------------------------'''.format(phone, password, period, quantity, typename)
