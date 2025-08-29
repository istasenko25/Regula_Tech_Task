import math
import random
import string
import time
import sys

class BloomFilter:

    def __init__(self, expected_items, false_positive_rate):

        if not (0 < false_positive_rate < 1):
            raise ValueError("false_positive_rate должен быть в диапазоне (0, 1)")

        if expected_items <= 0:
            raise ValueError("expected_items должно быть положительным числом")

        self.bit_array_size = int(- (expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2))
        self.number_hash_functions = round((self.bit_array_size / expected_items) * math.log(2))

        self.bit_map = [0] * self.bit_array_size  # создаём список нулей

    def _hash(self, item, k):
        try:
            return hash((item, k)) % self.bit_array_size
        except Exception as e:
            raise ValueError(f"Ошибка при хэшировании: {e}")

    def add_to_filter(self, item):
        for i in range(self.number_hash_functions):
            index = self._hash(item, i)
            self.bit_map[index] = 1  # отмечаем бит как установленный

    def contains_in_filter(self, item):
        for i in range(self.number_hash_functions):
            index = self._hash(item, i)
            if self.bit_map[index] == 0:
                return False  # хотя бы одного бита нет → точно не добавлялось
        return True  # возможно, добавлялось


class FileNames:

    def __init__(self, n):
        self.n = n
        self.max_length = 255

    def generate_fn(self):
        charset = string.ascii_letters + string.digits
        unique_names = set()

        while len(unique_names) < self.n:
            name = ''.join(random.choices(charset, k=self.max_length))
            unique_names.add(name)

        return list(unique_names)

def run_performance_test():
    num_files = 100000
    false_positive_rate = 0.01

    print(f"\nТест на {num_files} файлов с FPP = {false_positive_rate}:\n")

    #Время старта
    start = time.time()

    file_names = FileNames(num_files)
    file_list = file_names.generate_fn()

    #Время генерации файлов
    gen_time = time.time() - start

    #Время старта создания фильтра
    start_add = time.time()

    try:
        bloom_filter = BloomFilter(expected_items=num_files, false_positive_rate=false_positive_rate)
    except ValueError as e:
        print(f"Ошибка при создании фильтра Блума: {e}")
        return

    for i in file_list:
        bloom_filter.add_to_filter(i)

    #Время добавления в фильтр Блума
    add_time = time.time() - start_add

    memory_names = sys.getsizeof(file_list)
    memory_filter = sys.getsizeof(bloom_filter.bit_map)

    test_name = file_list[0]
    test_unknown = 'some_fake_file_' + ''.join(random.choices(string.ascii_letters, k=240))

    start_check = time.time()
    result_known = bloom_filter.contains_in_filter(test_name)
    time_known = time.time() - start_check

    start_check = time.time()
    result_unknown = bloom_filter.contains_in_filter(test_unknown)
    time_unknown = time.time() - start_check

    print(f"- Время генерации: {gen_time:.4f} сек")
    print(f"- Время добавления в фильтр: {add_time:.4f} сек")
    print(f"- Память под имена: {memory_names / 1024:.2f} КБ")
    print(f"- Память под фильтр: {memory_filter / 1024:.2f} КБ")
    print(f"- Проверка существующего: {time_known:.6f} сек → {result_known}")
    print(f"- Проверка несуществующего: {time_unknown:.6f} сек → {result_unknown}")

def main():
    try:
        run_performance_test()
    except Exception as e:
        print(f"Что-то пошло не так: {e}")

if __name__ == "__main__":
    main()



