
# YaMDb API

Проект YaMDb API это бэкенд сервис для сбора и публикации отзывов и комментариев пользоваталей на музыкальные произведения, книги и фильмы. Данный API можно использовать совмество с фронтенд для полноценного рейтингового сервиса.


## Installation

При первом запуске для функционирования проекта обязательно установить виртуальное окружение и выполнить миграции:

    $ python -m venv env
    $ source venv/Scripts/activate
    $ pip install -r requirements.txt

    
    $ python api_yamdb/manage.py makemigrations
    $ python api_yamdb/manage.py migrate
    $ python api_yamdb/manage.py runserver

После запуска проекта ознакомиться с документацией можно по ссылке http://127.0.0.1:8000/redoc/
    
## Authors

- [@sailormoon2111](https://github.com/sailormoon2111)

    Управление пользователями (Auth и Users): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения e-mail, поля.

- [@lordot](https://github.com/lordot)

    Категории (Categories), жанры (Genres) и произведения (Titles): модели, view и эндпойнты для них и рейтинги. Отзывы (Review) и комментарии (Comments): модели и view, эндпойнты, права доступа для запросов. Рейтинги произведений. Роль тимлидера.
