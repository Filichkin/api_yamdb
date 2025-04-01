from django.contrib import admin

from .models import Category, Titles, Genre


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'year', 'show_genres')
    list_filter = ('category', 'genre', 'year')
    search_fields = ('name', 'description')

    def show_genres(self, obj):
        return ", ".join([g.title for g in obj.genre.all()])
    show_genres.short_description = 'Жанры'
