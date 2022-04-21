"""
Классы и наследования.
Обработка исключений.
Импорт данных из csv файла.
Библиотеки csv, os.
"""
import csv
import os.path
from utils import *



class CarBase:
    cars_type = ["car", "truck", "spec_machine"]
    photo_file_types = []
    car_type = None

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying


class Car(CarBase):
    car_type = "car"

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count

    def get_photo_file_ext(self):
        return get_file_ext(self.photo_file_name)


class Truck(CarBase):
    car_type = "truck"

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.weight, self.height, self.lenght = self.__whl(body_whl)

    def __whl(self, body_whl):
        try:
            whl = body_whl.split("x")
            if len(whl) != 3:
                raise Exception("Неверный формат: ШИРИНАхДЛИНАхВЫСОТА")
            whl = list(map(float, whl))
        except:
            whl = [0.0, 0.0, 0.0]
        finally:
            return tuple(whl)

    def get_body_volume(self):
        return self.weight * self.height * self.lenght


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self._car_type = "spec_machine"
        self.extra = extra


def get_car_list(csv_filename):

    def _base_params_valid(current_car_params: dict):
        try:
            return bool(
                (current_car_params.get("car_type") in CarBase.cars_type) and
                (current_car_params.get("brand") != "") and
                (is_photo(current_car_params.get("photo_file_name"))) and
                (is_number(current_car_params.get("carrying")))
            )
        except Exception as e:
            print("Exception in _base_params_valid: ", e)
            return False

    def _car_params_valid(current_car_params: dict):
        try:
            return bool(is_int(current_car_params.get("passenger_seats_count")))
        except Exception as e:
            print(e)
            return False

    def _truck_params_valid(current_car_params: dict):
        try:
            return bool(True or current_car_params.get("body_whl") != "")
        except Exception as e:
            print(e)
            return False

    def spec_machine_params_valid(current_car_params: dict):
        try:
            return bool(True or current_car_params.get("extra") != "")
        except Exception as e:
            print(e)
            return False

    cars = []
    if os.path.isfile(csv_filename):
        with open(csv_filename) as f_obj:
            try:
                reader = csv.reader(f_obj, delimiter=';')
            except Exception as e:
                print("Exception: ", e)

            row_count = 0
            for row in reader:
                if row_count != 0:
                    current_car_params = dict()
                    column_count = 0
                    for item in row:
                        current_car_params[row_titles[column_count]] = item
                        column_count += 1
                    if _base_params_valid(current_car_params):
                        base_params = tuple()
                        if current_car_params.get("car_type") == "car" and _car_params_valid(current_car_params):
                            cars.append(Car(
                                current_car_params["brand"],
                                current_car_params["photo_file_name"],
                                current_car_params["carrying"],
                                current_car_params["passenger_seats_count"]
                            ))
                        elif current_car_params.get("car_type") == "truck" and _truck_params_valid(current_car_params):
                            cars.append(Car(
                                current_car_params["brand"],
                                current_car_params["photo_file_name"],
                                current_car_params["carrying"],
                                current_car_params["passenger_seats_count"]
                            ))
                        elif current_car_params.get("car_type") == "spec_machine" and spec_machine_params_valid(current_car_params):
                            cars.append(Car(
                                current_car_params["brand"],
                                current_car_params["photo_file_name"],
                                current_car_params["carrying"],
                                current_car_params["passenger_seats_count"]
                            ))
                else:
                    row_titles = row
                    row_count += 1
    return cars


cars = get_car_list(
    r"D:\HDD Project\Python\PythonCoursera\course1\data\w3_car_list.csv")

print(cars)
