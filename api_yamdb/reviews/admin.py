from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import Category, Comment, Genre, Review, Title, User


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


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    empty_value_display = '-пусто-'
    list_editable = ('text', 'author', 'score')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'author', 'text', 'pub_date')
    search_fields = ('text',)
    empty_value_display = '-пусто-'


@admin.register(User)
class CustomAdmin(UserAdmin):

    model = User
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bio',)}),
        ('Permissions', {'fields': ('role',)})
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        ('Permissions', {'fields': ('role',)})
    )

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitlesAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
