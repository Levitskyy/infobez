from Generator import Generator
import time

gnrt = Generator(12345)


def encode_file(filename_read: str, filename_write: str, keys: str):
    '''
    Функция считывает байты из заданного файла, применяет метод гаммирования к ним, используя генератор
    псевдослучайных чисел и записывает их в новый файл. Ключи для генератора указываются пользователем.
    '''
    start = time.time()
    # Применяем параметры из файла keys к генератору
    load_keys(gnrt, keys)
    with open(filename_read, 'rb') as fr:
        bytes_array = []
        while True:
            # Считывает 1 байт
            byte = fr.read(1)
            if not byte:
                break
            info_bits = int.from_bytes(byte, byteorder='big')
            # Генерируем псведослучайное число от 0 до 255
            random_number = gnrt.generate_number() % 256
            # Применяем операцию xor к байтам
            encoded_bits = info_bits ^ random_number
            bytes_array.append(encoded_bits)
    # Записываем новую последовательность байтов в заданный файл
    with open(filename_write, 'wb') as fw:
        bytes_seq = bytes(bytearray(bytes_array))
        fw.write(bytes_seq)
    # Рассчитываем время гаммирования и выводим его
    end = time.time() - start
    print('Время гаммирования: ', end)


def save_keys(gnrt: Generator, keyfile: str):
    '''
    Функция генерирует новые ключи в указанный пользователем файл
    '''
    if check_file_existance(keyfile + '.key'):
        print("Хотите заменить существующий файл?\n1) Да\n2) Нет")
        inp = int(input())
        if inp == 1:
            with open(keyfile + '.key', 'w') as f:
                gnrt.generate_new_seed(123459876)
                f.write(str(gnrt.a) + '\n' + str(gnrt.b) + '\n' + str(gnrt.current_number))
            return
        elif inp == 2:
            return
    else:
        with open(keyfile + '.key', 'w') as f:
            gnrt.generate_new_seed(123459876)
            f.write(str(gnrt.a) + '\n' + str(gnrt.b) + '\n' + str(gnrt.current_number))


def load_keys(gnrt: Generator, keyfile: str):
    '''
    Функция применяет ключи к текущему генератору из указанного файла
    '''
    with open(keyfile + '.key', 'r') as f:
        gnrt.a = int(f.readline())
        gnrt.b = int(f.readline())
        gnrt.current_number = int(f.readline())


def check_file_existance(file_path):
    '''
    Функция проверяет существование файла
    '''
    try:
        with open(file_path, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False


while True:
    # Цикл программы
    print('Выберите действие:\n1) Зашифровать файл\n2) Расшифровать файл\n3) Создать/Заменить файл с ключами\n')
    inp = int(input())
    if inp == 1:
        print('Введите название файла для шифрования: ')
        filename_read = input()
        print('Введите название зашифрованного файла: ')
        filename_write = input()
        print('Введите название файла-ключа: ')
        keys = input()
        encode_file(filename_read, filename_write, keys)
    if inp == 2:
        print('Введите название файла для расшифрования: ')
        filename_read = input()
        print('Введите название расшифрованного файла: ')
        filename_write = input()
        print('Введите название файла-ключа: ')
        keys = input()
        encode_file(filename_read, filename_write, keys)
    if inp == 3:
        print('Введите название файла-ключа: ')
        keys = input()
        save_keys(gnrt, keys)

