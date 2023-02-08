# YaMDb API

The YaMDb API project is a backend service for collecting and publishing user reviews and comments on music, books and films. This API can be used in conjunction with the frontend for a full-fledged rating service.


##Installation

At the first start, for the project to function, it is necessary to install a virtual environment and perform migrations:

     $ python -m venv env
     $ source venv/Scripts/activate
     $ pip install -r requirements.txt

    
     $ python api_yamdb/manage.py makemigrations
     $ python api_yamdb/manage.py migrate
     $ python api_yamdb/manage.py runserver

After starting the project, you can read the documentation at http://127.0.0.1:8000/redoc/
    
##Authors

- [@sailormoon2111](https://github.com/sailormoon2111)

     User management (Auth and Users): registration and authentication system, access rights, working with a token, e-mail confirmation system, fields.

- [@lordot](https://github.com/lordot)

     Categories (Categories), genres (Genres) and works (Titles): models, views and endpoints for them and ratings. Reviews (Review) and comments (Comments): models and views, endpoints, permissions for requests. Product ratings. The role of the team leader.
