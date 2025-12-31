"""
ID: 37
Тема: Two pointers
Название: Объединить два отсортированных массива
Сложность: Easy
--------------------------------------------------------------------------------
Условие:
Даны два отсортированных массива. Объединить их в один отсортированный массив.

Пример:
Вход: [1, 3, 5], [2, 4, 6]
Выход: [1, 2, 3, 4, 5, 6]
"""


def merge_arrays(arr1, arr2):
    res = []

    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            res.append(arr1[i])
            i += 1
        else:
            res.append(arr2[j])
            j += 1
        print(res)


    # Добавляем оставшиеся элементы
    while i < len(arr1):
        res.append(arr1[i])
        i += 1
    
    while j < len(arr2):
        res.append(arr2[j])
        j += 1

    return res


print(merge_arrays([1, 3, 5], [2, 4, 6]))
