"""
ID: 39
Тема: Two pointers
Название: Квадраты отсортированного массива
Сложность: Easy
--------------------------------------------------------------------------------
Условие:
Дан отсортированный массив целых чисел (может содержать отрицательные). Вернуть массив квадратов элементов в отсортированном порядке.

Пример:
Вход: [-4, -1, 0, 3, 10]
Выход: [0, 1, 9, 16, 100]
"""


def sort_squares(arr):
    n = len(arr)
    result = [0] * n

    l = 0
    r = n - 1
    pos = n - 1

    while l <= r:
        l_square = arr[l] * arr[l]
        r_square = arr[r] * arr[r]

        if l_square > r_square:
            result[pos] = l_square
            l += 1 
        else:
            result[pos] = r_square
            r -= 1

        pos -= 1
    
    return result


print(sort_squares([-4, -1, 0, 3, 10]))
