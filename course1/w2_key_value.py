"""
Работа с командной строкой. Парсинг комманд.
Библиотеки argparse, json.
Словарь. Работа со словарем.
"""
import argparse
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script KeyValue storage\n')

    parser.add_argument('path', help='provide a path')
    parser.add_argument('--key', default=None, help='provide a key')
    parser.add_argument('--value', default=None, help='provide a value')

    parser_arguments = parser.parse_args()
    ppath, pkey, pvalue = parser_arguments.path, parser_arguments.key, parser_arguments.value
else:
    pkey = "lasd"
    pvalue = "basd"

try:
    with open(ppath, 'r') as fsfile:
        json_data = fsfile.read()
except FileNotFoundError:
    print('Cant read/find the file')
else:
    if(pkey == None):
        print(json_data)
    else:
        try:
            dict_data = json.loads(json_data)
            tmp_value = dict_data.get(pkey)
            tuple_value = tmp_value if tmp_value != None else tuple()
        except Exception:
            if (len(json_data) == 0):
                dict_data = dict()
                tuple_value = tuple()
            else:
                print("json file is invalid")
                exit()
        if(pvalue == None):
            print(dict_data.get(pkey))
        elif(pkey != None and pvalue != None):
            tuple_value += tuple() if pvalue in tuple_value else (pvalue,)
            with open(ppath, 'w') as fsfile:
                dict_data.update({pkey: tuple_value})
                json_data = json.dumps(dict_data)
                fsfile.write(json_data)
