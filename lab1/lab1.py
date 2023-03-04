from typing import List
import copy


def split_text(text: str, column_key: List[int], row_key: List[int]) -> List[List[str]]:
    result = []
    column_key_len = len(column_key)
    row_key_len = len(row_key)
    for i, char in enumerate(text):
        column = column_key[i % column_key_len]
        row = row_key[i // column_key_len % row_key_len]
        result.append((row, column, char))
    number_of_blocks = 8

    blocks = []
    for i in range(number_of_blocks):
        blocks.append([])

    for item in result:
        k = len(column_key) * (item[0] - 1) + item[1]
        blocks[k - 1].append(item[2])
    return blocks


def reconstruct_text(blocks: List[List[str]], column_key: List[int], row_key: List[int]) -> str:
    result = ""
    temp_blocks = copy.deepcopy(blocks)
    count = 0
    while count < len(temp_blocks):
        for i in range(len(row_key)):
            for j in range(len(column_key)):
                k = len(column_key) * (row_key[i] - 1) + column_key[j]
                if len(temp_blocks[k - 1]) == 0:
                    count += 1
                    continue
                result += temp_blocks[k - 1].pop(0)
    return result


text = ""
column_key = []
row_key = []
result = []
while True:
    operation = 0
    while operation == 0:
        print("Выберите операцию:\n1) Разбиение\n2) Сборка")
        x = int(input())
        if x == 1:
            operation = 1
        elif x == 2:
            operation = 2

    if operation == 1:
        print("Введите текстовую строку: ")
        text = input()

    while True:
        flag = False
        print("Введите ключи столбцов через пробел (4 ключа в диапазоне 1-4): ")
        try:
            column_key = list(map(int, input().split()))
        except ValueError:
            continue
        if len(column_key) != 4:
            flag = True
        else:
            for i in column_key:
                if i < 1 or i > 4:
                    flag = True
        if flag:
            continue
        else:
            break

    while True:
        flag = False
        print("Введите ключи строк через пробел (2 ключа в диапазоне 1-2): ")
        try:
            row_key = list(map(int, input().split()))
        except ValueError:
            continue
        if len(row_key) != 2:
            flag = True
        else:
            for i in row_key:
                if i < 1 or i > 2:
                    flag = True
        if flag:
            continue
        else:
            break

    if operation == 1:
        result = split_text(text, column_key, row_key)
        for i, c in enumerate(result):
            print(i + 1, c)

    elif operation == 2:
        text = reconstruct_text(result, column_key, row_key)
        print(text)


