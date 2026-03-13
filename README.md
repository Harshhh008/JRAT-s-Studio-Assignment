# Prod E-commerce Website

### Step 1 : Python Env setup + packages

`python -m venv venv`

`venv/Scripts/activate`

+ install requirement packages

`pip install django`

`pip install pillow` # for working with media file

`pip install python-decouple` # for working with secret data

`pip install django-debug-toolbar` # for debugging django querysets

`pip install django-browser-reload` # for auto reloading django pages if any changes occurs


### Step 2 : Project Setup.

1. account -> which is contains all authentication related logics
2. products -> which is contains all product related logics
3. cart -> which is contains all cart related logics
4. order -> which is contains order related logics and payments
5. dashboard -> for admin user and staff