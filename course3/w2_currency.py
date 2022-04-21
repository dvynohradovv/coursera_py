import xml.etree.ElementTree as ET
from decimal import Decimal

import requests


def convert(amount, cur_from, cur_to, date, requests):
    def __rub_to(_amount, _cur_to, _date, _requests):
        response = _requests.get("http://cbr.ru/scripts/XML_daily.asp",
                                 params={"date_req": _date})  # Использовать переданный
        root = ET.fromstring(response.text)
        for valute in root.findall("Valute"):
            if valute.find("CharCode").text == _cur_to:
                _amount = Decimal(_amount)
                value = Decimal(valute.find("Value").text.replace(',', '.'))
                nominal = Decimal(valute.find("Nominal").text)
                rate = _amount / value * nominal
                return rate

    if cur_from == "RUB":
        return __rub_to(amount, cur_to, date, requests).quantize(Decimal("1.0000"))
    one_rub_to_cur_from = __rub_to(1, cur_from, date, requests)
    rub_in_cur_from = Decimal(amount) / one_rub_to_cur_from
    return __rub_to(rub_in_cur_from, cur_to, date, requests).quantize(Decimal("1.0000"))


if __name__ == "__main__":
    print(convert(Decimal("1000.1000"), 'ZAR', 'KRW', "26/02/2018", requests))  # 92628.4452
