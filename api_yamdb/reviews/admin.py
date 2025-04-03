from django.contrib import admin

from .models import Category, Title, Genre


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'year', 'show_genres')
    list_filter = ('category', 'genre', 'year')
    search_fields = ('name', 'description')

    def show_genres(self, obj):
        return ", ".join([genre.title for genre in obj.genre.all()])

    show_genres.short_description = 'Жанры'
