import random
import argparse
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django

django.setup()

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Subject, Commendation
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

COMMENDATIONS = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!'
]


def fix_marks(schoolkid):
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid)
    Mark.objects.filter(schoolkid=schoolkid, points__lt=4).ubdate.points = 5


def delete_comments(schoolkid):
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid)
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject):
    schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid)
    year_of_study = schoolkid.year_of_study
    group_letter = schoolkid.group_letter
    subject = Subject.objects.get(title=subject, year_of_study=year_of_study)
    lessons = Lesson.objects.filter(subject=subject, year_of_study=year_of_study, group_letter=group_letter)
    while True:
        lesson = lessons.order_by('?').first()
        lesson_teacher = lesson.teacher
        lesson_date = lesson.date
        text = random.choice(COMMENDATIONS)
        if not Commendation.objects.filter(schoolkid=schoolkid, subject=subject, teacher=lesson_teacher):
            Commendation.objects.create(
                text=text,
                created=lesson_date,
                schoolkid=schoolkid,
                subject=subject,
                teacher=lesson_teacher
            )
            break


def create_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('''\
СКРИПТ ПОЗВОЛЯЕТ:
* исправить - оценки; удалить - замечания от учителей; добавить - похвалу от учителя.
-------------------------------------------------------------------------------------
Для исправления неудовлетворительных оценок (двоек и троек),
удаления замечаний от учителей, добавления похвалы:
--fix_marks - Исправление неудовлетворительных оценок (двоек и троек) на пятерки.
--deleting_comments - Удаление замечаний от учителей.
--create_commendation - Добавления похвалы от учителя
-------------------------------------------------------------------------------------'''
                     )
    )
    parser.add_argument('-n', '--name', default='Фролов Иван Григорьевич',
                        help='Введите Фамилию Имя Отчество ученика.')
    parser.add_argument('-s', '--subject', default='Математика',
                        help="Введите название предмета")
    parser.add_argument('-fix_marks', default=False, action='store_true',
                        help="Исправление неудовлетворительных оценок (двоек и троек) на пятерки")
    parser.add_argument('-deleting_comments', default=False, action='store_true',
                        help="Удаление замечаний от учителей")
    parser.add_argument('-create_commendation', default=False, action='store_true',
                        help="Добавления похвалы от учителя")
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    try:
        if args.fix_marks:
            fix_marks(args.name)
        if args.deleting_comments:
            delete_comments(args.name)
        if args.create_commendation:
            create_commendation(args.name, args.subject)
    except Schoolkid.DoesNotExist:
        print('Такого ученика нет, проверьте правильность ввода!')
    except Subject.DoesNotExist:
        print('Такого предмета нет, проверьте правильность ввода!')
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено сразу несколько таких учеников!')
