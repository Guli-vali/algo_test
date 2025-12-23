#!/usr/bin/env python3
"""
Скрипт для тренировки по асинхронности и конкурентности.
Использование:
    python async_trainer.py              # Случайный вопрос/упражнение
    python async_trainer.py --answer 1   # Показать ответ на вопрос с id=1
    python async_trainer.py -a 1         # То же самое
    python async_trainer.py --list       # Показать все вопросы
    python async_trainer.py --topic "Основы async/await"  # Вопрос из темы
    python async_trainer.py --type theory  # Только теоретические вопросы
"""

import json
import random
import argparse
import sys
from pathlib import Path


def load_questions(file_path='async_questions.json'):
    """Загрузить вопросы из JSON файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('questions', [])
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден!")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Ошибка: неверный формат JSON в файле {file_path}!")
        sys.exit(1)


def print_question(question):
    """Красиво вывести вопрос/упражнение."""
    print("=" * 80)
    
    # Иконка в зависимости от типа
    type_icons = {
        'theory': '📚',
        'practice': '💡',
        'exercise': '💻',
        'code_analysis': '🔍'
    }
    icon = type_icons.get(question['type'], '❓')
    
    print(f"{icon} ID: {question['id']} | Тип: {question['type']} | Тема: {question['topic']}")
    print(f"📝 {question['title']}")
    print("-" * 80)
    
    # Выводим вопрос или условие задачи
    if 'question' in question:
        print("ВОПРОС:")
        print(question['question'])
    elif 'description' in question:
        print("УСЛОВИЕ:")
        print(question['description'])
    else:
        print("СОДЕРЖАНИЕ:")
        print(question.get('content', ''))
    
    print("=" * 80)
    print(f"\n💡 Чтобы увидеть ответ, выполните: python {sys.argv[0]} --answer {question['id']}")


def print_answer(question):
    """Красиво вывести ответ."""
    print("=" * 80)
    print(f"✅ ОТВЕТ НА ВОПРОС #{question['id']}: {question['title']}")
    print("=" * 80)
    
    if 'answer' in question:
        print(question['answer'])
    elif 'solution' in question:
        print("РЕШЕНИЕ:")
        print(question['solution'])
    else:
        print("Ответ не найден.")
    
    print("=" * 80)


def get_random_question(questions, filter_type=None, filter_topic=None):
    """Получить случайный вопрос с опциональными фильтрами."""
    filtered = questions
    
    if filter_type:
        filtered = [q for q in filtered if q['type'] == filter_type]
    
    if filter_topic:
        filtered = [q for q in filtered if q['topic'] == filter_topic]
    
    if not filtered:
        print("Ошибка: нет доступных вопросов с указанными фильтрами!")
        if filter_type:
            print(f"Тип: {filter_type}")
        if filter_topic:
            print(f"Тема: {filter_topic}")
        sys.exit(1)
    
    return random.choice(filtered)


def get_question_by_id(questions, question_id):
    """Получить вопрос по ID."""
    for question in questions:
        if question['id'] == question_id:
            return question
    return None


def list_all_questions(questions):
    """Вывести список всех вопросов."""
    print("=" * 80)
    print("СПИСОК ВСЕХ ВОПРОСОВ И УПРАЖНЕНИЙ")
    print("=" * 80)
    
    # Группировка по типам и темам
    by_type_topic = {}
    for question in questions:
        q_type = question['type']
        topic = question['topic']
        key = (q_type, topic)
        if key not in by_type_topic:
            by_type_topic[key] = []
        by_type_topic[key].append(question)
    
    # Иконки для типов
    type_icons = {
        'theory': '📚',
        'practice': '💡',
        'exercise': '💻',
        'code_analysis': '🔍'
    }
    
    for (q_type, topic), type_questions in sorted(by_type_topic.items()):
        icon = type_icons.get(q_type, '❓')
        print(f"\n{icon} {q_type.upper()} | {topic} ({len(type_questions)} вопросов):")
        for question in sorted(type_questions, key=lambda x: x['id']):
            print(f"  [{question['id']:3d}] {question['title']}")
    
    print("\n" + "=" * 80)
    print(f"Всего вопросов: {len(questions)}")
    
    # Статистика по типам
    type_counts = {}
    for question in questions:
        q_type = question['type']
        type_counts[q_type] = type_counts.get(q_type, 0) + 1
    
    print("\nСтатистика по типам:")
    for q_type, count in sorted(type_counts.items()):
        print(f"  {q_type}: {count}")
    
    print("=" * 80)


def get_available_topics(questions):
    """Получить список доступных тем."""
    return sorted(set(q['topic'] for q in questions))


def get_available_types(questions):
    """Получить список доступных типов."""
    return sorted(set(q['type'] for q in questions))


def main():
    parser = argparse.ArgumentParser(
        description='Тренажер по асинхронности и конкурентности для подготовки к собеседованиям',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s                    # Показать случайный вопрос/упражнение
  %(prog)s --answer 42         # Показать ответ на вопрос с ID=42
  %(prog)s -a 42               # То же самое (короткая форма)
  %(prog)s --list              # Показать список всех вопросов
  %(prog)s --topic "Основы async/await"  # Случайный вопрос из указанной темы
  %(prog)s --type theory       # Только теоретические вопросы
  %(prog)s --type exercise     # Только практические упражнения
        """
    )
    
    parser.add_argument(
        '--answer', '-a',
        type=int,
        metavar='ID',
        help='Показать ответ на вопрос с указанным ID'
    )
    
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='Показать список всех вопросов'
    )
    
    parser.add_argument(
        '--topic',
        type=str,
        help='Выбрать случайный вопрос из указанной темы'
    )
    
    parser.add_argument(
        '--type',
        type=str,
        choices=['theory', 'practice', 'exercise', 'code_analysis'],
        help='Фильтр по типу вопроса (theory, practice, exercise, code_analysis)'
    )
    
    parser.add_argument(
        '--file',
        type=str,
        default='async_questions.json',
        help='Путь к файлу с вопросами (по умолчанию: async_questions.json)'
    )
    
    args = parser.parse_args()
    
    # Загрузить вопросы
    questions = load_questions(args.file)
    
    # Обработка команд
    if args.list:
        list_all_questions(questions)
    elif args.answer is not None:
        question = get_question_by_id(questions, args.answer)
        if question:
            print_answer(question)
        else:
            print(f"Ошибка: вопрос с ID={args.answer} не найден!")
            sys.exit(1)
    elif args.topic:
        topic_questions = [q for q in questions if q['topic'] == args.topic]
        if topic_questions:
            question = get_random_question(topic_questions, filter_type=args.type)
            print_question(question)
        else:
            print(f"Ошибка: тема '{args.topic}' не найдена!")
            print("\nДоступные темы:")
            for topic in get_available_topics(questions):
                print(f"  - {topic}")
            sys.exit(1)
    elif args.type:
        # Случайный вопрос указанного типа
        question = get_random_question(questions, filter_type=args.type)
        print_question(question)
    else:
        # Случайный вопрос
        question = get_random_question(questions)
        print_question(question)


if __name__ == '__main__':
    main()


