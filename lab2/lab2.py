import math
from random import randint


def encode_sequence(sequence: str):
    '''
    функция, которая кодирует входную двоичную последовательность с использованием кода Хэмминга.
    Входные данные должны быть в виде строки.
    '''
    if len(sequence) == 0:
        return
    # Вычисляем количество битов, которые нужно добавить к последовательности для резерва
    # Это значение округляется до ближайшей степени двойки
    reserve_len = math.ceil(math.log2(len(sequence)))
    # Если новая длина последовательности (с учетом добавленных битов резерва) больше,
    # чем 2 в степени резервной длины, увеличиваем резервную длину на 1
    if (len(sequence) + reserve_len) > (1 << reserve_len):
        reserve_len += 1
    if len(sequence) == 1:
        reserve_len = 2
    if len(sequence) == 2:
        reserve_len = 3

    encoded_seq_width = reserve_len + len(sequence)
    encoded_sequence = [0 for x in range(encoded_seq_width)]
    string_sequence = ''

    parity_bit_position = 1
    current_inf_bit = 0
    # Заполняем массив информационными битами
    for i in range(encoded_seq_width):
        if i != parity_bit_position - 1:
            encoded_sequence[i] = int(sequence[current_inf_bit])
            current_inf_bit += 1
        else:
            parity_bit_position *= 2

    # Создаем матрицу проверки четности
    a_matrix = create_matrix(reserve_len, encoded_seq_width)

    print("Матрица шифрования:")
    for i in a_matrix:
        print(i)

    # Вычисляем значения проверочных битов
    for i in range(reserve_len):
        for j in range(encoded_seq_width):
            if (encoded_sequence[j] == 1) and (a_matrix[i][j] == 1):
                encoded_sequence[(2 ** i) - 1] = int(not(encoded_sequence[(2 ** i) - 1]))

    # Добавляем дополнительный бит четности
    extra_parity_bit = 0
    for i in range(encoded_seq_width):
        if encoded_sequence[i] == 1:
            extra_parity_bit = int(not(extra_parity_bit))
        string_sequence += str(encoded_sequence[i])
    string_sequence = str(extra_parity_bit) + string_sequence

    # Возвращаем закодированную последовательность
    return string_sequence


def decode_sequence(sequence: str):
    '''
    принимает на вход закодированную последовательность в виде строки.
    Функция декодирует последовательность и выводит результат,
    который содержит исправленное сообщение или информацию об ошибке в последовательности.
    '''
    # Получаем значение дополнительного бита четности и удаляем его из последовательности.
    extra_parity_bit = int(sequence[0])
    sequence_wo_extra = sequence[1:]
    inf_bits = []

    parity_bit_pos = 1
    # Удаляем резервные биты из последовательности
    for i in range(len(sequence_wo_extra)):
        if i != parity_bit_pos - 1:
            inf_bits.append(sequence_wo_extra[i])
        else:
            parity_bit_pos *= 2

    # Генерируем новую зашифрованную последовательность из полученных информационных битов
    temp_sequence = encode_sequence(''.join(str(i) for i in inf_bits))
    temp_sequence_wo_extra = temp_sequence[1:]

    error_sum = 0
    sum = 0

    parity_bit_pos = 1
    # Считаем позицию ошибки
    for i in range(len(sequence_wo_extra)):
        if i == parity_bit_pos - 1:
            if temp_sequence_wo_extra[i] != sequence_wo_extra[i]:
                error_sum += parity_bit_pos
            parity_bit_pos *= 2
        sum += int(sequence_wo_extra[i])
    sum += extra_parity_bit

    corrected_msg = ''

    parity_bit_pos = 1
    # Исправляем ошибку
    for i in range(len(sequence_wo_extra)):
        if i != parity_bit_pos - 1:
            if i == error_sum - 1:
                corrected_msg += str(int(not(sequence_wo_extra[i])))
            else:
                corrected_msg += str(sequence_wo_extra[i])
        else:
            parity_bit_pos *= 2

    # Проверки на количество ошибок и вывод
    if (sum % 2 == 0) and (error_sum != 0):
        print("Двойная ошибка")
        return
    if (sum % 2 == 1) and (error_sum != 0):
        print("Ошибка на позиции " + str(error_sum + 1))
        print("Исправленное сообщение: " + corrected_msg)
        return
    print("Нет ошибок")
    print("Сообщение: " + corrected_msg)
    return


def create_matrix(reserve_len: int, matrix_width: int):
    '''
    Функция создает матрицу нужной размерности с позициями, которые контролируют резервные биты
    '''
    result_matrix = [[0 for x in range(matrix_width)] for x in range(reserve_len)]

    for i in range(reserve_len):
        last_bit = 0
        temp_i = 2 ** i
        for j in range(matrix_width):
            if (j + 1) % temp_i == 0:
                result_matrix[i][j] = int(not last_bit)
            else:
                result_matrix[i][j] = last_bit
            last_bit = result_matrix[i][j]
    return result_matrix


while True:
    print("Введите последовательность битов для шифрования: ")
    bits = input()
    encoded = encode_sequence(bits)
    print("Зашифрованное сообщение: ")
    print(encoded)
    print("Введите сообщение для расшифровки: ")
    decode_sequence(input())
