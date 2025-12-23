#!/usr/bin/env python3
"""
Скрипт для работы с задачами по алгоритмам.
Использование:
    python task_selector.py              # Случайная задача
    python task_selector.py --solution 1 # Показать решение задачи с id=1
    python task_selector.py -s 1         # То же самое
    python task_selector.py --list      # Показать все задачи
"""

import json
import random
import argparse
import sys
from pathlib import Path


def load_tasks(file_path='tasks.json'):
    """Загрузить задачи из JSON файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('tasks', [])
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден!")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Ошибка: неверный формат JSON в файле {file_path}!")
        sys.exit(1)


def print_task(task):
    """Красиво вывести задачу."""
    print("=" * 80)
    print(f"ID: {task['id']}")
    print(f"Тема: {task['topic']}")
    print(f"Название: {task['title']}")
    print(f"Сложность: {task['difficulty']}")
    print("-" * 80)
    print("Условие:")
    print(task['description'])
    print("=" * 80)


def print_solution(task):
    """Красиво вывести решение задачи."""
    print("=" * 80)
    print(f"РЕШЕНИЕ ЗАДАЧИ #{task['id']}: {task['title']}")
    print("=" * 80)
    print(task['solution'])
    print("=" * 80)


def get_random_task(tasks):
    """Получить случайную задачу."""
    if not tasks:
        print("Ошибка: нет доступных задач!")
        sys.exit(1)
    return random.choice(tasks)


def get_task_by_id(tasks, task_id):
    """Получить задачу по ID."""
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None


def list_all_tasks(tasks):
    """Вывести список всех задач."""
    print("=" * 80)
    print("СПИСОК ВСЕХ ЗАДАЧ")
    print("=" * 80)
    
    # Группировка по темам
    by_topic = {}
    for task in tasks:
        topic = task['topic']
        if topic not in by_topic:
            by_topic[topic] = []
        by_topic[topic].append(task)
    
    for topic, topic_tasks in sorted(by_topic.items()):
        print(f"\n📚 {topic} ({len(topic_tasks)} задач):")
        for task in sorted(topic_tasks, key=lambda x: x['id']):
            print(f"  [{task['id']:3d}] {task['title']} ({task['difficulty']})")
    
    print("\n" + "=" * 80)
    print(f"Всего задач: {len(tasks)}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description='Генератор задач по алгоритмам для подготовки к собеседованиям',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s                    # Показать случайную задачу
  %(prog)s --solution 42       # Показать решение задачи с ID=42
  %(prog)s -s 42               # То же самое (короткая форма)
  %(prog)s --list              # Показать список всех задач
  %(prog)s --topic "Two pointers"  # Случайная задача из указанной темы
        """
    )
    
    parser.add_argument(
        '--solution', '-s',
        type=int,
        metavar='ID',
        help='Показать решение задачи с указанным ID'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='Показать список всех задач'
    )
    
    parser.add_argument(
        '--topic',
        type=str,
        help='Выбрать случайную задачу из указанной темы'
    )
    
    parser.add_argument(
        '--file',
        type=str,
        default='tasks.json',
        help='Путь к файлу с задачами (по умолчанию: tasks.json)'
    )
    
    args = parser.parse_args()
    
    # Загрузить задачи
    tasks = load_tasks(args.file)
    
    # Обработка команд
    if args.list:
        list_all_tasks(tasks)
    elif args.solution is not None:
        task = get_task_by_id(tasks, args.solution)
        if task:
            print_solution(task)
        else:
            print(f"Ошибка: задача с ID={args.solution} не найдена!")
            sys.exit(1)
    elif args.topic:
        topic_tasks = [t for t in tasks if t['topic'] == args.topic]
        if topic_tasks:
            task = random.choice(topic_tasks)
            print_task(task)
        else:
            print(f"Ошибка: тема '{args.topic}' не найдена!")
            print("\nДоступные темы:")
            topics = set(t['topic'] for t in tasks)
            for topic in sorted(topics):
                print(f"  - {topic}")
            sys.exit(1)
    else:
        # Случайная задача
        task = get_random_task(tasks)
        print_task(task)
        print(f"\n💡 Чтобы увидеть решение, выполните: python {sys.argv[0]} --solution {task['id']}")


if __name__ == '__main__':
    main()
