# Tasks

## Account (Authentication setup)

###  Custom User Model (custom : with email)

- [x] create custom manager to handle login with email
- [x] create custom user model
- [x] create address model to handle multiple address of user
- [x] change global user model with custom user model inside settings.py
- [x] initialize all account / models inside account / admin

### Custom Forms

- [x] template setup for working with forms
- [x] create custom user register form
- [x] create custom login form
- [] profile form
- [] address form

### urls 
- [x] create account/urls.py file to manage account urls endpoints.

### views

- [x] create register view
- [x] create login view
- [x] create logout view
- [] create dashboard (for admin access) -> CURD operation with products
- [] create profile view
- [] change password
- [] reset password

## Debug and auto reload setup

- [x] Django debug toolbar setup
- [x] Django auto reload browser setup

## Product (product related operations)

### model

- [x] category model setup fields (id, name, created_at, updated_at)
- [x] product model setup fields (id, name, category(foreign_key), description, quantity, price, created_at, updated_at)
- [x] product image model setup fields (id, image, product(foreign_key), created_at, updated_at)

### views

- [] create product
- [] update product
- [] delete product
- [] list of all product
- [] get product details(unique)

## Media File setup for working with images in development

- [x] configure media files root inside settings.py
- [x] attach root path with url so we can see images inside browser

## Custom commands

- [x] create utils apps for making some functionality or automation works.
- [x] create folder management/commands for working with cli commands
- [x] create custom commands for running makemigrations, migrate, superuser automatically