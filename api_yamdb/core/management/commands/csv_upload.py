import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import (
    Title,
    Genre,
    Category,
    Review,
    Comment,
)
from users.models import User


class Command(BaseCommand):
    ERROR_MESSAGE = 'Ошибка - {error}, проблема в строке - {row}.'
    DONE_MESSAGE = 'Данные из {file} перенесены в таблицу {model}.'

    MODELS_FILES = {
        User: 'users.csv',
        Category: 'category.csv',
        Genre: 'genre.csv',
        Title: 'titles.csv',
        Review: 'review.csv',
        Comment: 'comments.csv',
    }

    DIFFERENT_FIELDS = {
        Review: ['author', 'author_id'],
        Comment: ['author', 'author_id'],
        Title: ['category', 'category_id'],
    }

    help = 'Запись в БД данных из csv-файлов'

    def handle(self, *args, **kwargs):
        for model, file in self.MODELS_FILES.items():
            with open(
                f'static/data/{file}', 'rt', encoding='utf-8'
            ) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if model in self.DIFFERENT_FIELDS:
                        row = {
                            field_csv.replace(
                                self.DIFFERENT_FIELDS[model][0],
                                self.DIFFERENT_FIELDS[model][1],
                            ): field_table
                            for field_csv, field_table in row.items()
                        }
                    try:
                        model.objects.create(**row)
                    except Exception as error:
                        raise CommandError(
                            self.ERROR_MESSAGE.format(error=error, row=row)
                        )

                self.stdout.write(
                    self.DONE_MESSAGE.format(
                        file=file, model=model._meta.model_name
                    )
                )
