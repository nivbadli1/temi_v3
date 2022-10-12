# Callme Temi App

Nurses have their hands full, but now they have even more missions to keep up with. 
Residents who live at retirement homes, can not be able to communicate with their families,
Because they may not have the cognitive ability to speak.
Nurses should take care of that each resident communicate with his family.
This is where CallMeTemi app enters the picture.
CallMeTemi is an application for nurses help their to keep communication of
residents and their families using temi robot that calls their families automatically. <br />

> Features

- `Bootstrap 5 Design`: **[Argon Dashboard](https://www.creative-tim.com/product/argon-dashboard?AFFILIATE=128200)**
- `Up-to-date dependencies`
- `DB Tools`: SQLAlchemy ORM, Flask-Migrate (schema migrations) , Pandas 
- Session-Based authentication (via **flask_login**), Forms validation
- python package for controlling temi robot 
- Google Calendar Api integration
- Pytemi package for controlling temi robot by using websocket protocol
<br />


## ✨ Code-base structure

The project is coded using blueprints, app factory pattern, dual configuration profile (development and production) and an intuitive structure presented bellow:

```bash
< PROJECT ROOT >
   |
   |-- apps/
   |    |
   |    |-- home/                           # A simple app that serve HTML files
   |    |    |-- routes.py                  # Define app routes
   |    |
   |    |-- authentication/                 # Handles auth routes (login and register)
   |    |    |-- routes.py                  # Define authentication routes  
   |    |    |-- models.py                  # Defines models  
   |    |    |-- forms.py                   # Define auth forms (login and register) 
   |    |    |-- __init__.py                # Initialize authentication methods
   |    |    |-- util.py                    # Utility methods
   |    |
   |    |-- core/                           # Handles core classes (scheduler service and departments)
   |    |    |-- __init__.py                # Initialize core methods
   |    |    |-- classes.py                 # Define classes for corr objects 
   |    |    |-- scheduler_service.py       # run schedular service task
   |    |    |-- util.py                    # Utility methods
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>          # CSS files, Javascripts files
   |    |
   |    |-- templates/                      # Templates used to render pages
   |    |    |-- includes/                  # HTML chunks and components
   |    |    |    |-- navigation.html       # Top menu component
   |    |    |    |-- sidebar.html          # Sidebar component
   |    |    |    |-- footer.html           # App Footer
   |    |    |    |-- scripts.html          # Scripts common to all pages
   |    |    |
   |    |    |-- layouts/                   # Master pages
   |    |    |    |-- base-fullscreen.html  # Used by Authentication pages
   |    |    |    |-- base.html             # Used by common pages
   |    |    |
   |    |    |-- accounts/                  # Authentication pages
   |    |    |    |-- login.html            # Login page
   |    |    |    |-- register.html         # Register page
   |    |    |
   |    |    |-- home/                      # UI Kit Pages
   |    |         |-- index.html            # Index page
   |    |         |-- 404-page.html         # 404 page
   |    |         |-- *.html                # All other pages
   |    |    
   |  config.py                             # Set up the app
   |    __init__.py                         # Initialize the app
   |
   |-- requirements.txt                     # App Dependencies
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- run.py                               # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />
