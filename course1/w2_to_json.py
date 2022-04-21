"""
Работа с json файлами.
"""
import json


def dec_to_json(func):
    def wrapped(*arg, **kwargs):
        result = func(*arg, **kwargs)
        try:
            json_result = json.dumps(result)
            return json_result
        except Exception:
            print("We have some problems")
            return result
    return wrapped

# get_data = dec_to_json(get_data)(key, value) => wrapped(key, value) = > {key:value}


@dec_to_json
def get_data(key, value):
    return {key: value}


print(get_data("Dima", "ONU"))  # вернёт '{"data": 42}'
