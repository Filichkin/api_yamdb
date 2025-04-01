from django.contrib import admin


from .models import Titles, Genres, TitleGenre, Categories, Reviews, Comments


@admin.register(Titles)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ('name', 'year')
    list_filter = ('name',)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'title',
        'text',
        'score',
        'pub_date'
    )
    list_filter = ('author',)


admin.site.register(Genres)
admin.site.register(TitleGenre)
admin.site.register(Categories)
admin.site.register(Comments)
