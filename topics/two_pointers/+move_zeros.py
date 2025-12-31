"""
ID: 34
Тема: Two pointers
Название: Переместить нули в конец
Сложность: Easy
--------------------------------------------------------------------------------
Условие:
Дан массив. Переместить все нули в конец, сохранив относительный порядок остальных элементов.

Пример:
Вход: [0, 1, 0, 3, 12]
Выход: [1, 3, 12, 0, 0]
"""

def zeros_switch(arr):
    write_ix = 0

    for read_ix in range(len(arr)):
        if arr[read_ix] != 0:
            arr[write_ix] = arr[read_ix]
            write_ix += 1
        
    while write_ix < len(arr):
        arr[write_ix] = 0
        write_ix += 1

    return arr

print(zeros_switch([0, 1, 0, 3, 12]))
