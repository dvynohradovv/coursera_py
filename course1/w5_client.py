"""
Клиент для отправки метрик.

"""
import socket
import time

from utils import *


class ClientError(Exception):
    """Собственное исключение класса Client"""

    def __init__(self, message="ClientError"):
        self.message = message

    def __str__(self):
        return self.message


class Client:
    """ Класс клиент"""

    def __init__(self, host: str, port: int, timeout: int = None):
        """ Инициализация клиента"""
        self.__adress = (host, port)
        if not is_number(timeout):
            timeout = None
        # cоздание сокета базовый вариант
        """
            sock = socket.socket()
            sock.connect(("127.0.0.1", 10001))
        """
        # создание сокета альтернативный вариант
        self.__sock = socket.create_connection(
            self.__adress, timeout)

    def put(self, metric: str, value: float, timestamp: int = None):
        """ Запрос к серверу на отправку данных """
        if not is_number(timestamp):
            timestamp = str(int(time.time()))

        request = "put {0} {1} {2}\n".format(metric, value, timestamp)
        process_response = self.__request_response(request)

    def get(self, metric: str):
        """ Запрос к серверу на получение данных """
        def _to_dict(process_response: str):
            response_keyValue = {}
            if process_response:
                try:
                    for metric_it in process_response:
                        metric_it = metric_it.split(" ")

                        key = metric_it[0]  # metric
                        value = (int(metric_it[2]),  # timestamp
                                 float(metric_it[1]))  # value
                        user_metric_value = []
                        if response_keyValue.get(key):
                            user_metric_value = response_keyValue.get(key)
                        user_metric_value.append(value)

                        response_keyValue[key] = user_metric_value
                except:
                    raise ClientError()
            return response_keyValue

        request = "get {0}\n".format(metric)
        process_response = self.__request_response(request)

        return _to_dict(process_response)

    def __request_response(self, request: str):
        """ Отправка запроса, получение ответа и обработка ответа от сервера"""
        def _process_data(data: str):
            """Обработка ответа"""
            # <статус ответа><\n><данные ответа><\n\n>
            if data.startswith(("ok", "error")) and data.endswith("\n\n"):
                resp_ls = data.split('\n')
                # статус ответа
                resp_status = resp_ls.pop(0)
                # удаляю \n эллементы
                resp_ls.pop()
                resp_ls.pop()
                # проверка данных ответа
                if len(resp_ls):
                    if resp_status == "ok":
                        return resp_ls
                    elif resp_status == "error":
                        pass
                elif resp_status == "ok":
                    return
            raise ClientError()

        # send request
        self.__sock.sendall(request.encode("utf8"))
        # get data
        data = self.__sock.recv(4096)
        return _process_data(data.decode("utf-8"))


def main():
    client = Client("127.0.0.1", 8888, timeout=15)
    client.put("palm.cpu", 0.5, timestamp=1150864247)
    client.put("palm.cpu", 2.0, timestamp=1150864248)
    client.put("palm.cpu", 0.5, timestamp=1150864248)
    client.put("eardrum.cpu", 3, timestamp=1150864250)
    client.put("eardrum.cpu", 4, timestamp=1150864251)
    client.put("eardrum.memory", 4200000)
    print(client.get("*"))


if __name__ == "__main__":
    main()
