"""
ID: 35
Тема: Two pointers
Название: Три числа с суммой равной нулю
Сложность: Medium
--------------------------------------------------------------------------------
Условие:
Дан массив целых чисел. Найти все уникальные тройки чисел, сумма которых равна нулю.

Пример:
Вход: [-1, 0, 1, 2, -1, -4]
Выход: [[-1, -1, 2], [-1, 0, 1]]

"""

def three_sum(nums):
    """
    Каноническое решение задачи Three Sum.
    Время: O(n²), Пространство: O(1) (без учета результата)
    """
    result = []
    nums.sort()
    
    for i in range(len(nums) - 2):
        # Пропускаем дубликаты для первого элемента
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Ранний выход: если минимальная сумма уже больше 0
        if nums[i] > 0:
            break
        
        left = i + 1
        right = len(nums) - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # Пропускаем дубликаты для обоих указателей
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    return result


# Тестирование
if __name__ == "__main__":
    print(three_sum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
