import datetime
import psutil


class Generator:
    a = 0
    b = 0
    currentNumber = 0
    m = 2 ** 24

    def __init__(self, a: int, b: int, c0: int):
        self.currentNumber = c0
        self.a = a
        self.b = b

    def set_seed(self, a: int, b: int, c0: int):
        self.currentNumber = c0
        self.a = a
        self.b = b

    def generate_number(self):
        generated_number = (self.a * self.currentNumber + self.b) % self.m
        self.currentNumber = generated_number
        return generated_number


def find_gcd(a: int, b: int) -> int:
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    return a + b


def find_coprime(number: int):
    while (find_gcd(number, 2 ** 24) != 1) and (number % 2 == 0):
        number += 1
    return number


def find_a(a: int):
    while a % 4 != 1:
        a += 1
    return a


def main():
    now = datetime.datetime.now()
    ms = now.microsecond
    a = find_a(ms)
    b = find_coprime(psutil.virtual_memory().available)
    gnrt1 = Generator(a, b, 1123415163412586763453)
    for i in range(10):
        nm = gnrt1.generate_number()
        print(nm)


if __name__ == '__main__':
    main()
