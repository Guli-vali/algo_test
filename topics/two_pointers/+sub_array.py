"""
ID: 38
Тема: Two pointers
Название: Проверить, является ли строка подпоследовательностью другой
Сложность: Easy
--------------------------------------------------------------------------------
Условие:
Даны две строки s и t. Проверить, является ли s подпоследовательностью t.

Пример:
Вход: s = "ace", t = "abcde"
Выход: True

Вход: s = "axc", t = "ahbgdc"
Выход: False
"""


def sub_string_check(s_string, t_string):
    i = 0
    j = 0
    while j < len(t_string):
        if t_string[j] == s_string[i]:
            i += 1
        j += 1
    
    if i == len(s_string):
        return True
    
    return False


print(sub_string_check("ace", "abcde"))
print(sub_string_check("axc", "ahbgdc"))
