import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import (
    Titles,
    Genres,
    Categories,
    Reviews,
    Comments,
)
from users.models import User


class Command(BaseCommand):
    ERROR_MESSAGE = 'Ошибка - {error}, проблема в строке - {row}.'
    DONE_MESSAGE = 'Данные из {file} перенесены в таблицу {model}.'

    MODELS_FILES = {
        User: 'users.csv',
        Categories: 'category.csv',
        Genres: 'genre.csv',
        Titles: 'titles.csv',
        Reviews: 'review.csv',
        Comments: 'comments.csv',
    }

    DIFFERENT_FIELDS = {
        Reviews: ['author', 'author_id'],
        Comments: ['author', 'author_id'],
        Titles: ['category', 'category_id'],
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
