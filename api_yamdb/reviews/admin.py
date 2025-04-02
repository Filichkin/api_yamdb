from django.contrib import admin

from .models import Title, Genre, Category, Review, Comment


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ('name', 'year')
    list_filter = ('name',)


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'text',
        'score',
        'pub_date'
    )
    list_filter = ('author',)


admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Comment)
