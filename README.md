# LittleLemon
Django REST API project for restaurant
This project is a **restaurant management REST API** created for the **Backend Professional Certificate** by **Meta**.  
It allows different user roles (Admin, Manager, Delivery Crew, Customer) to interact with the system according to their permissions.

## User Roles & Permissions

| Group/User  | Permissions / Actions                                           |
|------------|-----------------------------------------------------------------|
| Admin      | Full access to all models via Django Admin                      |
| Manager    | CRUD on Categories and Menu Items                                |
| Delivery   | View and update orders assigned to them                         |
| Customer   | Register, login, browse menu, add items to cart, place orders  |

## API Endpoints

### Authentication (Djoser)

- Register: /auth/users/
- Login (get token): /auth/token/login/
- Logout: /auth/token/logout/
- Current user info: /auth/users/me/

### Categories

- List & Create: /api/categories/
  - Admin only can create
  - Everyone can list

### Menu Items

- List & Create: /api/menu-items/
  - Manager/Admin can POST
  - Everyone can GET
- Update item of the day: /api/menu-items/<id>/update/

### Cart (Customer)

- List & Add: /api/cart/

### Orders

- List & Create: /api/orders/
- Manager assigns delivery crew: /api/orders/<id>/assign/
- Delivery crew updates order status: /api/orders/<id>/deliver/

### Notes

- This project uses Django, Django REST Framework, and Djoser for authentication.
- Database: SQLite (db.sqlite3 included for testing).
