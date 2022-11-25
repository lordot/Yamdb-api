from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import Category, Comment, Genre, Review, Title, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'slug')


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')
    search_fields = ('name', 'category')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'category')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    empty_value_display = '-пусто-'
    list_editable = ('text', 'author', 'score')


@admin.register(Comment)
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
        ('Role', {'fields': ('role',)}),
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        ('Role', {'fields': ('role',)}),
    )

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    ]
