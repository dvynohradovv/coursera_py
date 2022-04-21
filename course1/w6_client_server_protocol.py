import asyncio


class ClientServerProtocol(asyncio.Protocol):

    __user_metric_keyValue = {}

    def connection_made(self, transport: tuple):
        """ Клиент подключился к серверу """
        self.transport = transport

    def data_received(self, request: bytes):
        """ Получены данные от клиента """

        def _process_request(request: str):
            """ Обработка данных от клиента """
            def process_put_request(request: list):
                """ Обработка запроса put-данных от клиента """
                response_to_client = []
                if len(request) == 3:
                    try:
                        new_key = request[0]  # metric
                        new_value = (
                            float(request[1]),  # metric_value
                            int(request[2])  # timestamp
                        )
                    except:
                        pass
                    user_metric_value = []
                    if ClientServerProtocol.__user_metric_keyValue.get(new_key) is not None:
                        user_metric_value = ClientServerProtocol.__user_metric_keyValue.get(
                            new_key)

                        # проверяем чтоб не было > 1 значения в секунду
                        counter = 0
                        found = False
                        for metric_value, timestamp in user_metric_value:
                            if timestamp == new_value[1]:
                                # если есть, то меняем на новое значение
                                user_metric_value[counter] = new_value
                                found = True
                                break
                            counter += 1

                        if not found:
                            user_metric_value.append(new_value)
                        user_metric_value.sort(
                            key=lambda timestamp: timestamp[1])
                    else:
                        # добавляем значение в лист, если лист пустой
                        user_metric_value.append(new_value)
                    ClientServerProtocol.__user_metric_keyValue[new_key] = user_metric_value
                    # запрос успешно обработан
                    response_to_client.append("ok")
                return response_to_client

            def process_get_request(request: list):
                """ Обработка запроса get-данных от клиента """
                response_to_client = []
                if len(request) == 1:
                    # в любом случае, запрос успешен, даже если ключей нету
                    response_to_client.append("ok")
                    metric_name = request[0]
                    if metric_name == "*":
                        for key, value in ClientServerProtocol.__user_metric_keyValue.items():
                            for metric_value, timestamp in value:
                                metric = f"{key} {metric_value} {timestamp}"
                                response_to_client.append(metric)
                    else:
                        if ClientServerProtocol.__user_metric_keyValue.get(metric_name) is not None:
                            for metric_value, timestamp in ClientServerProtocol.__user_metric_keyValue.get(metric_name):
                                metric = f"{metric_name} {metric_value} {timestamp}"
                                response_to_client.append(metric)
                return response_to_client

            response_to_client = []
            if request.startswith(("put", "get")) and request.endswith("\n"):
                # удаляю \n символ в конце
                # ! request_ls.pop() - не правильно
                request = request[:-1]
                request_ls = request.split(" ")
                # забираю тип запроса
                req_type = request_ls.pop(0)
                if len(request_ls):
                    if req_type == "put":
                        response_to_client = process_put_request(request_ls)
                    elif req_type == "get":
                        response_to_client = process_get_request(request_ls)
            if not len(response_to_client):
                response_to_client.append("error")
                response_to_client.append("wrong command")

            response = "\n".join(response_to_client) + "\n\n"
            return response

        response = _process_request(request.decode())
        self.transport.write(response.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        print("Запустился сервер")
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
