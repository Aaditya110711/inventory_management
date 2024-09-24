# Inventory Management System API

This project is a backend API for an Inventory Management System built with Django Rest Framework. It supports CRUD operations on inventory items, integrated with JWT-based authentication for secure access.

## Features

CRUD operations for inventory items
- JWT authentication
- Redis caching for improved performance
- PostgreSQL database
- Logging for debugging and monitoring


## Setup
1. Clone the repository:

```github
git clone https://github.com/Aaditya110711/inventory_management.git
cd inventory-management
```
2. Create a virtual environment and activate it: 
```bash
python -m venv venv
source venv/bin/activate  
```
3. Install the required packages:
```bash
pip install -r requirements.txt
```
4. Set up the PostgreSQL database and update the DATABASES configuration in settings.py with your database credentials.
5. Set up Redis and update the CACHES configuration in settings.py if necessary
6. Run migrations:
```bash
python manage.py migrate
```
7. Create a superuser:
```bash
python manage.py createsuperuser
```
8. Run the development server:
```bash
python manage.py runserver
```



## API Endpoints

### Authentication

- POST /api/auth/register/: Register a new user
- POST /api/auth/login/: Obtain JWT tokens
- POST /api/auth/login/refresh/: Refresh JWT token
- POST /api/auth/logout/: Logout (blacklist refresh token)

### Inventory Items

- GET /api/items/: List all inventory items
- POST /api/items/: Create a new inventory item
- GET /api/items/{id}/: Retrieve a specific inventory item
- PUT /api/items/{id}/: Update a specific inventory item
- DELETE /api/items/{id}/: Delete a specific inventory item


### Test

Run the unit tests with:
```bash
python manage.py test
```



### Postman Testing
To test the API in Postman, follow these steps:
#### Register a new user:

-  Method: POST
- URL: http://localhost:8000/api/auth/register/
- Body (raw JSON):
```json
{
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword"
}
```


#### Login to obtain JWT tokens:

- Method: POST
- URL: http://localhost:8000/api/auth/login/
- Body (raw JSON):
```json
{
    "username": "testuser",
    "password": "testpassword"
}
```


#### Use the obtained access token for subsequent requests by adding it to the Authorization header:

- Header: Authorization: Bearer <your_access_token>


#### Create an inventory item:

- Method: POST
- URL: http://localhost:8000/api/items/
- Body (raw JSON):
```json
{
    "name": "Test Item",
    "description": "This is a test item",
    "quantity": 10
}
```

#### Retrieve all inventory items:

- Method: GET
- URL: http://localhost:8000/api/items/


#### Retrieve a specific inventory item:

- Method: GET
- URL: http://localhost:8000/api/items/{id}/


#### Update an inventory item:

- Method: PUT
- URL: http://localhost:8000/api/items/{id}/
- Body (raw JSON):
```json
{
    "name": "Updated Test Item",
    "description": "This is an updated test item",
    "quantity": 15
}
```



#### Delete an inventory item:

- Method: DELETE
- URL: http://localhost:8000/api/items/{id}/



Remember to replace {id} with the actual ID of the inventory item you want to retrieve, update, or delete.

