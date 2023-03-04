import math
from random import randint


def encode_sequence(sequence: str):
    if len(sequence) == 0:
        return
    reserve_len = math.ceil(math.log2(len(sequence)))
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
    for i in range(encoded_seq_width):
        if i != parity_bit_position - 1:
            encoded_sequence[i] = int(sequence[current_inf_bit])
            current_inf_bit += 1
        else:
            parity_bit_position *= 2

    a_matrix = create_matrix(reserve_len, encoded_seq_width)

    for i in range(reserve_len):
        for j in range(encoded_seq_width):
            if (encoded_sequence[j] == 1) and (a_matrix[i][j] == 1):
                encoded_sequence[(2 ** i) - 1] = int(not(encoded_sequence[(2 ** i) - 1]))

    extra_parity_bit = 0
    for i in range(encoded_seq_width):
        if encoded_sequence[i] == 1:
            extra_parity_bit = int(not(extra_parity_bit))
        string_sequence += str(encoded_sequence[i])
    string_sequence = str(extra_parity_bit) + string_sequence

    return string_sequence


def decode_sequence(sequence: str):
    extra_parity_bit = int(sequence[0])
    sequence_wo_extra = sequence[1:]
    inf_bits = []

    parity_bit_pos = 1
    for i in range(len(sequence_wo_extra)):
        if i != parity_bit_pos - 1:
            inf_bits.append(sequence_wo_extra[i])
        else:
            parity_bit_pos *= 2

    temp_sequence = encode_sequence(''.join(str(i) for i in inf_bits))
    temp_sequence_wo_extra = temp_sequence[1:]

    error_sum = 0
    sum = 0

    parity_bit_pos = 1
    for i in range(len(sequence_wo_extra)):
        if i == parity_bit_pos - 1:
            if temp_sequence_wo_extra[i] != sequence_wo_extra[i]:
                error_sum += parity_bit_pos
            parity_bit_pos *= 2
        sum += int(sequence_wo_extra[i])
    sum += extra_parity_bit

    corrected_msg = ''

    parity_bit_pos = 1
    for i in range(len(sequence_wo_extra)):
        if i != parity_bit_pos - 1:
            if i == error_sum - 1:
                corrected_msg += str(int(not(sequence_wo_extra[i])))
            else:
                corrected_msg += str(sequence_wo_extra[i])
        else:
            parity_bit_pos *= 2

    if (sum % 2 == 0) and (error_sum != 0):
        print("Double error")
        return
    if (sum % 2 == 1) and (error_sum != 0):
        print("Error on pos " + str(error_sum + 1))
        print("Correct message: " + corrected_msg)
        return
    print("No errors")
    print("Message: " + corrected_msg)
    return


def create_matrix(reserve_len: int, matrix_width: int):
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
    bits = input()
    encoded = encode_sequence(bits)
    print(encoded)
    decode_sequence(input())
