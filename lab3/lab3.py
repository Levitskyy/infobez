import datetime
import psutil
import math
import matplotlib.pyplot as plt


class Generator:
    a = 0
    b = 0
    current_number = 0
    m = 2 ** 24

    def __init__(self, c0: int):
        '''
        Конструктор, который генерирует новые ключи для генератора
        '''
        self.generate_new_seed(c0)

    def set_seed(self, a: int, b: int, c0: int):
        '''
        Функция применяет к генератору определенные пользователем ключи
        '''
        self.current_number = c0
        self.a = a
        self.b = b

    def generate_new_seed(self, c0: int):
        '''
        Функция генерирует новые ключи
        '''
        now = datetime.datetime.now()
        ms = now.microsecond
        a = find_a(ms)
        # для псевдослучайного значения b требуется библиотека psutil, которая позволит получать текущее значения
        # свободной оперативной памяти
        b = find_coprime(psutil.virtual_memory().available)
        #b = find_coprime(a * 12341257)
        self.set_seed(a, b, c0)

    def set_c0(self, c0: int):
        '''
        Функция изменяет текущее число в генераторе
        '''
        self.current_number = c0

    def set_other_generator_seed(self, gnrt):
        '''
        Функция копирует параметры другого генератора в текущий
        '''
        gnrt.current_number = self.current_number
        gnrt.a = self.a
        gnrt.b = self.b

    def generate_number(self):
        '''
        Функция генерирует псевдослучайное число на основе текущих параметров
        '''
        generated_number = (self.a * self.current_number + self.b) % self.m
        self.current_number = generated_number
        return generated_number


class Stats:
    frequency = [0 for x in range(100)]
    part = math.floor(2 ** 24 / 100)
    min_freq = 1.01
    max_freq = -1.0

    def __init__(self):
        '''
        Создает массив из сотни отрезков
        '''
        self.frequency = [0 for x in range(100)]

    def add_value(self, value: int):
        '''
        Добавляет значение в определенный отрезок в массиве
        '''
        try:
            self.frequency[value // self.part] += 1
        except IndexError:
            self.frequency[99] += 1

    def get_stats_array(self):
        '''
        Выводит массив отрезков
        '''
        print(self.frequency)

    def get_frequency(self, values_amount: int):
        '''
        Показывает статистику попаданий чисел в определенные отрезки
        '''
        # подсчитаем относительные частоты попадания в каждый интервал
        relative_frequencies = [count / values_amount for count in self.frequency]

        # вычислим среднее арифметическое от относительных частот
        mean_relative_frequency = sum(relative_frequencies) / len(relative_frequencies)

        # округлим относительные частоты
        rounded_relative_frequencies = [round(freq, 4) for freq in relative_frequencies]

        # вывод гистограммы
        y = rounded_relative_frequencies
        x = [i for i in range(100)]
        default_x_ticks = range(len(x))
        plt.bar(x, self.frequency, align='center')
        plt.xlabel('Bins')
        plt.ylabel('Frequency')
        #plt.ylim(0, 0.05)
        plt.show()

        print("Средняя относительная частота:", round(mean_relative_frequency, 4))
        print("Минимальная относительная частота:", min(rounded_relative_frequencies))
        print("Максимальная относительная частота:", max(rounded_relative_frequencies))
        print("Относительные частоты попадания в интервалы:", rounded_relative_frequencies)




def find_gcd(a: int, b: int) -> int:
    '''
    Функция находит НОД
    '''
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    return a + b


def find_coprime(number: int):
    '''
    Функция находит взаимно простое число с 2^24
    '''
    while (find_gcd(number, 2 ** 24) != 1) and (number % 2 == 0):
        number += 1
    return number


def find_a(a: int):
    '''
    Функция возвращает первое подходящее число для ключа a
    '''
    while a % 4 != 1:
        a += 1
    return a


def write_file(gnrt: Generator, amount: int):
    '''
    Функция записывает определенное кол-во псевдослучайных чисел в файл numbers.txt
    и выводит статистику
    '''
    stats = Stats()
    with open('numbers.txt', 'w') as f:
        for i in range(amount):
            new_value = gnrt.generate_number()
            stats.add_value(new_value)
            f.write(str(new_value) + '\n')
    stats.get_frequency(amount)


def main():
    # Цикл программы
    c0_console = 123456789
    c0 = 123456789
    gnrt = Generator(c0)
    while True:
        print("Выберите действие:\n1) Сгенерировать число на экран\n2) Сгенерировать n чисел в файл\n3) Изменить порождающее число последовательности\n4) Поставить новые параметры ГСПЧ\n")
        chosen = int(input())
        if chosen == 1:
            gnrt.set_c0(c0_console)
            print(gnrt.generate_number())
            c0_console = gnrt.current_number
        if chosen == 2:
            gnrt.set_c0(c0)
            print("Сколько чисел вы хотите сгенерировать: ")
            amount = int(input())
            write_file(gnrt, amount)
        if chosen == 3:
            print("Напишите новое число: ")
            c0 = int(input())
            c0_console = c0
            c0_file = c0
        if chosen == 4:
            gnrt.generate_new_seed(987654321)
            c0 = gnrt.current_number
            c0_console = gnrt.current_number


if __name__ == '__main__':
    main()