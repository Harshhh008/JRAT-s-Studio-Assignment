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
- [x] profile form
- [x] address form
- [x] order data in profile

### urls 
- [x] create account/urls.py file to manage account urls endpoints.

### views

- [x] create register view
- [x] create login view
- [x] create logout view
- [x] create dashboard (for admin access) -> CURD operation with products
- [x] create profile view
- [x] change password
- [x] reset password

## Debug and auto reload setup

- [x] Django debug toolbar setup
- [x] Django auto reload browser setup

## Product (product related operations)

### model

- [x] category model setup fields (id, name, created_at, updated_at)
- [x] product model setup fields (id, name, category(foreign_key), description, quantity, price, created_at, updated_at)
- [x] product image model setup fields (id, image, product(foreign_key), created_at, updated_at)

### views

- [x] create product
- [x] update product
- [x] delete product
- [x] crud operation on category
- [x] list of all product
- [x] get product details(unique)
- [x] add url in html file for unique product add image
- [x] search product by category name and product name

## Media File setup for working with images in development

- [x] configure media files root inside settings.py
- [x] attach root path with url so we can see images inside browser

## Custom commands

- [x] create utils apps for making some functionality or automation works.
- [x] create folder management/commands for working with cli commands
- [x] create custom commands for running makemigrations, migrate, superuser automatically

## Cart Functionality

- [x] create app cart
- [x] model : cart(unique for each user) and cartitem(store products + unique_cart_id)
- [x] view cart functionality
- [x] add to cart product functionality
- [x] delete product from cart functionality
- [] session based cart # bug : item total and total not working
- [] udate cart_item after login or register

## Order Functionality

- [x] model : order(every time generated new if order placed (foreign key)), order item(store all items from the cart), payment
- [x] payment integration (paypal)
- [x] send mail purchase success

  flow : cart_items -> checkout -> create_order(storedata) -> if payment success -> cp all cart_item to order_item -> redirect payment complete page


## pagination
- [x] pagination in list product 

## messages for every view (success or failed)

- [x] messages

## analytics (total sale, top products)

- [x] total sale
- [x] top products

# handle form errors