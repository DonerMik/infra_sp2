import os
import csv

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from reviews.models import User, Category, Genre, Title, Review, Comment


class Command(BaseCommand):
    help = 'Loading data into the database'

    def handle(self, *args, **kwargs):
        print(settings.BASE_DIR)

        DATAFILES_DIRS = os.path.join(settings.STATICFILES_DIRS[0], 'data/')
        file_name = DATAFILES_DIRS + 'users.csv'
        if os.path.exists(file_name):
            print('Импорт Users')
            count = 0
            with open(file_name, "r", encoding="utf8") as fin:
                cin = csv.reader(fin)
                items = [row for row in cin]
                for i in range(1, len(items)):
                    item = items[i]
                    role = ''
                    for j in range(len(User.ROLE)):
                        if User.ROLE[j][1] == item[3]:
                            role = User.ROLE[j][0]
                            break
                    if role == '':
                        CommandError(f'Ошибка данных поля role {item[3]} позиция {i} ')

                    _, created = User.objects.get_or_create(
                        id=item[0],
                        username=item[1],
                        email=item[2],
                        role=role,
                        bio=item[4],
                        first_name=item[5],
                        last_name=item[6]
                    )
                    if created:
                        count += 1
                print(f'Записей : {len(items)-1}\n'
                      f'Создано : {count}')
        else:
            CommandError(f'Файл {file_name} не найден')

        file_name = DATAFILES_DIRS + 'category.csv'
        if os.path.exists(file_name):
            print('Импорт Category')
            count = 0
            with open(file_name, "r", encoding="utf8") as fin:
                cin = csv.reader(fin)
                items = [row for row in cin]
                for i in range(1, len(items)):
                    item = items[i]
                    _, created = Category.objects.get_or_create(
                        id=item[0],
                        name=item[1],
                        slug=item[2],
                    )
                    if created:
                        count += 1
                print(f'Записей : {len(items)-1}\n'
                      f'Создано : {count}')
        else:
            CommandError(f'Файл {file_name} не найден')

        file_name = DATAFILES_DIRS + 'genre.csv'
        if os.path.exists(file_name):
            print('Импорт Genre')
            count = 0
            with open(file_name, "r", encoding="utf8") as fin:
                cin = csv.reader(fin)
                items = [row for row in cin]
                for i in range(1, len(items)):
                    item = items[i]
                    _, created = Genre.objects.get_or_create(
                        id=item[0],
                        name=item[1],
                        slug=item[2],
                    )
                    if created:
                        count += 1
                print(f'Записей : {len(items)-1}\n'
                      f'Создано : {count}')

        file_name = DATAFILES_DIRS + 'titles.csv'
        if os.path.exists(file_name):
            print('Импорт Title')
            count = 0
            with open(file_name, "r", encoding="utf8") as fin:
                cin = csv.reader(fin)
                items = [row for row in cin]

                for i in range(1, len(items)):
                    item = items[i]
                    category = Category.objects.get(id=item[3])
                    _, created = Title.objects.get_or_create(
                        id=item[0],
                        name=item[1],
                        year=item[2],
                        category=category,
                    )
                    if created:
                        count += 1
                print(f'Записей : {len(items)-1}\n'
                      f'Создано : {count}')

        file_name = DATAFILES_DIRS + 'genre_title.csv'
        if os.path.exists(file_name):
            print('Импорт Genre_Title')
            count = 0
            with open(file_name, "r", encoding="utf8") as fin:
                cin = csv.reader(fin)
                items = [row for row in cin]
                for i in range(1, len(items)):
                    item = items[i]
                    if not Title.objects.filter(id=item[1], genre__id=item[2]):
                        title = Title.objects.get(id=item[1])
                        genre = Genre.objects.get(id=item[2])
                        title.genre.add(genre)
                        count += 1
                print(f'Записей : {len(items)-1}\n'
                      f'Создано : {count}')

        file_name = DATAFILES_DIRS + 'review.csv'
        if os.path.exists(file_name):
            print('Импорт Review')
            count = 0
            with open(file_name, "r", encoding="utf8") as fin:
                cin = csv.reader(fin)
                items = [row for row in cin]
                for i in range(1, len(items)):
                    item = items[i]
                    try:
                        _ = Review.objects.get(id=item[0])
                    except Review.DoesNotExist:
                        title = Title.objects.get(id=item[1])
                        author = User.objects.get(id=item[3])
                        Review.objects.create(
                            id=item[0],
                            title=title,
                            text=item[2],
                            author=author,
                            score=item[4],
                            pub_date=item[5]
                        )
                        count += 1
                print(f'Записей : {len(items)-1}\n'
                      f'Создано : {count}')

        file_name = DATAFILES_DIRS + 'comments.csv'
        if os.path.exists(file_name):
            print('Импорт Comment')
            count = 0
            with open(file_name, "r", encoding="utf8") as fin:
                cin = csv.reader(fin)
                items = [row for row in cin]
                for i in range(1, len(items)):
                    item = items[i]
                    try:
                        _ = Comment.objects.get(id=item[0])
                    except Comment.DoesNotExist:
                        review = Review.objects.get(id=item[1])
                        author = User.objects.get(id=item[3])
                        Comment.objects.create(
                            id=item[0],
                            review=review,
                            text=item[2],
                            author=author,
                            pub_date=item[4]
                        )
                        count += 1
                print(f'Записей : {len(items)-1}\n'
                      f'Создано : {count}')
