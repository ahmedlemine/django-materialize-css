# Django Materialize CSS and HTMx Starter Template
### a simple Django blog with [Materialize CSS](https://materializecss.com/) and [HTMx](https://htmx.org/)


This is a fully functioning mobile-first Django project to use as a starter for your new project.
The fully responsive mobile-first design with a side menu and floating action buttons make the whole site look like an Android app.

A Posts app and Accounts app are setup just as an example to show case various functionaliy and featuers of the project with several useful packages and settings included like Django-Allauth and Django-Jazzmin.

### Features:
- Materialize CSS gives a Googles Material Design look and feel (Android) for all pages, with floating action buttons.
- Fully responsive and mobile-first design with a side menu that makes the whole site on phones look like an Android app.
- HTMx for posting comments wich allows for only updating the part of the page that shows the comment. After posting a new comment, a "delete" icon is shown next to it so that it can be deleted, also without reloading the entire page.
- HTMx for loading posts asynchronously in the home page.
- Posts app for publishing blog posts with a blog photo.
- Comments system to allow user to comment on posts.
- Custom user model ready to use. You can add custom fields and properties to users.
- User login/signup with Django-Allauth with all Allauth templates customized to have Materilized CSS style.
- User email/password change with email confirmation.
- User public and private profile with photo and bio and list of posts.
- Flash messages (toasts) that look like Android native flash messages to display info after any user generated action like "Post has been updated", "You're logged in as User" etc.



### Installed Packages:
- django-allauth setup and ready to use with login and profiles.
- django-environ to store senstive settings out of the project.
- django-hitcount for counting visits to blog posts or any models you wish to add later.
- django-imagekit
- django-jazzmin for a nicer looking Django admin interface.
- django-materializecss-form to add support for Materialize CSS in Django forms.


### How to use:
1- clone repo and cd into it:

```
git clone <repo/repo>
cd <repo_dir>
```

2- create virtual environment:

```
python3 -m venv venv
```

3- Activate virtual env:

```
source venv/bin/activate
```

4- install requirements

```
pip3 install -r requirements.txt
```

5- migrate:

```
python3 manage.py maigrate
```

6- create suepr user:

```
python3 manage.py createsuperuser
```

7- run server

```
python3 manage.py runserver
```

8- start your own apps (or use it just as a blog):

```
python3 manage.py startapp my_app
```
