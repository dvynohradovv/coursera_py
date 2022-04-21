"""
Работа с магическими методами. Переопределение методов.
Библиотеки uuid, os, tempfile
"""
import os.path
import tempfile
import uuid


class File:

    def __init__(self, path: str):
        self.path = path
        if os.path.isfile:
            self.write("")

    def __add__(self, other):
        new_file_text = self.read() + other.read()

        tmp_dir = tempfile.gettempdir()
        # uuid - Generate a random UUID
        tmp_filename = str(uuid.uuid4())

        path = os.path.join(tmp_dir, tmp_filename)
        with open(path, 'w') as file:
            file.write(new_file_text)
        return File(path)

    def __str__(self):
        return self.path

    def __iter__(self):
        self._free_samples = self.read().splitlines()
        return self

    def __next__(self):
        if self._free_samples:
            return self._free_samples.pop()
        else:
            raise StopIteration("All free samples have been dispensed.")

    def read(self):
        with open(self.path, 'r') as file:
            return file.read()

    def write(self, text: str):
        with open(self.path, 'w') as file:
            file.write(text)


path_to_file = 'some_filename'
os.path.exists(path_to_file)
file_obj = File(path_to_file)
os.path.exists(path_to_file)
file_obj.read()
file_obj.write('some text')
file_obj.read()
file_obj.write('other text')
file_obj.read()
file_obj_1 = File(path_to_file + '_1')
file_obj_2 = File(path_to_file + '_2')
file_obj_1.write('line 1\n')
file_obj_2.write('line 2\n')
new_file_obj = file_obj_1 + file_obj_2
isinstance(new_file_obj, File)
print(new_file_obj)
for line in new_file_obj:
    print(ascii(line))
