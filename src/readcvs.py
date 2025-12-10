import argparse
import csv
from tabulate import tabulate
from collections import defaultdict
import sys


def read_csv_files(file_paths):
    """Читает данные из нескольких CSV файлов и объединяет их"""
    all_data = []

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    all_data.append(row)
        except FileNotFoundError:
            print(f"Ошибка:{file_path}", file=sys.stderr)
            sys.exit(1)
    return all_data


def generate_performance_report(data):
    """Генерирует отчет performance"""
    # Словарь для хранения сумм performance и количества записей по позициям
    position_stats = defaultdict(lambda: {'sum': 0, 'count': 0})

    # Собираем статистику по позициям
    for row in data:
        position = row.get('position', 'Unknown')
        performance_str = row.get('performance', '0')

        try:
            performance = float(performance_str)
            position_stats[position]['sum'] += performance
            position_stats[position]['count'] += 1
        except (ValueError, TypeError):
            # Пропускаем некорректные значения
            continue

    # Вычисляем средние значения и формируем отчет
    report = []
    for position, stats in position_stats.items():
        if stats['count'] > 0:
            average_performance = stats['sum'] / stats['count']
            report.append({
                'position': position,
                'average_performance': round(average_performance, 2)
            })

    # Сортируем по убыванию средней эффективности
    report.sort(key=lambda x: x['average_performance'], reverse=True)

    return report


def main():
    parser = argparse.ArgumentParser(description='Генерация отчетов по выполненным задачам')
    parser.add_argument('--files', nargs='+', required=True, help='Список CSV файлов с данными')
    parser.add_argument('--report', choices=['performance'], required=True,
                        help='Тип отчета: performance')

    args = parser.parse_args()

    # Читаем данные из всех файлов
    data = read_csv_files(args.files)

    if not data:
        print("Нет данных для формирования отчета", file=sys.stderr)
        sys.exit(1)

    # Генерируем запрошенный отчет
    if args.report == 'performance':
        report_data = generate_performance_report(data)

        # Форматируем отчет для вывода
        if report_data:
            headers = ["", 'Position', 'Performance']
            table_data = []
            for i, item in enumerate(report_data, start=1):
                table_data.append([
                    i,
                    item['position'],
                    item['average_performance']
                ])

            print(tabulate(table_data, headers=headers, tablefmt='grid',
                           floatfmt=".2f", stralign='left', numalign='right'))
        else:
            print("Нет данных для отчета performance")


if __name__ == '__main__':
    main()
