import datetime

# Генератор из лабороторной №3
class Generator:
    a = 0
    b = 0
    current_number = 0
    m = 2 ** 24

    def __init__(self, c0: int):
        self.generate_new_seed(c0)

    def set_seed(self, a: int, b: int, c0: int):
        self.current_number = c0
        self.a = a
        self.b = b

    def generate_new_seed(self, c0: int):
        now = datetime.datetime.now()
        ms = now.microsecond
        a = find_a(ms)
        #b = find_coprime(psutil.virtual_memory().available)
        b = find_coprime(a * 12341257)
        self.set_seed(a, b, c0)

    def set_c0(self, c0: int):
        self.current_number = c0

    def set_other_generator_seed(self, gnrt):
        gnrt.current_number = self.current_number
        gnrt.a = self.a
        gnrt.b = self.b

    def generate_number(self):
        generated_number = (self.a * self.current_number + self.b) % self.m
        self.current_number = generated_number
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
    return


if __name__=='__main__':
    main()