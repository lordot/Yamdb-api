from django.contrib import admin

from .models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'slug')


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')
    search_fields = ('name', 'category')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitlesAdmin)
