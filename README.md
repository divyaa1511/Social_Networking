# Social Networking Application

This is a social networking application built using Django and Django Rest Framework (DRF). The application provides functionalities for user signup, login, sending/accepting/rejecting friend requests, listing friends, listing pending friend requests, and searching users by email or name.


## Features

- User Signup
- User Login
- Send Friend Request
- Accept Friend Request
- Reject Friend Request
- List Friends
- List Pending Friend Requests
- Search Users by Email or Name


## Requirements

- Python 3.8+
- Django 5.0.6
- Django Rest Framework 3.15.1
- Docker (for containerization)


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/divyaa1511/Social_Networking.git
   cd social
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   
4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   
5. Run database migrations:
   ```bash
   python manage.py migrate

6. Create a superuser to access the Django admin:
   ```bash
   python manage.py createsuperuser
   
8. Start the development server:
   ```bash
   python manage.py runserver


## API Endpoints

### 1. User Signup
 
URL :   /api/signup/

Method: POST
 ```bash
Body:
{
    "email": "user@example.com",
    "username": "user123",
    "password": "password123"
}
```

### 2. User Login

URL : /api/login/

Method: POST
 ```bash
Body:
{
    "email": "user@example.com",
    "password": "password123"
}
 ```

### 3. Send Friend Request

URL: /api/send-friend-request/

Method: POST
 ```bash
Body:
{
    "receiver_id": 2
}
 ```
### 4. Accept Friend Request

URL: /api/accept-friend-request/

Method: POST
 ```bash
Body:
{
    "sender_id": 2
}
 ```

### 5. Reject Friend Request

URL: /api/reject-friend-request/

Method: POST
 ```bash
Body:
{
    "sender_id": 2
}
 ```

### 6. List Friends

URL: /api/friends/

Method: GET

### 7. List Pending Friend Requests

URL: /api/pending-friend-requests/

Method: GET

### 8. Search Users

URL: /api/search-users/

Method: GET

Parameters: ?query=<search_query>


## Running with Docker

Build the Docker image:
 ```bash
docker-compose build
 ```
Run the Docker containers:
 ```bash
docker-compose up
 ```

The application should now be running in a Docker container and accessible at http://localhost:8000.

## Postman Collection
The Postman collection for this project is available in the postman directory. You can import the collection into Postman to test the API endpoints.

## License
Save this content to a file named `README.md` in your project root directory. This file provides an overview of the project, installation instructions, API endpoints, and additional information like how to run the project with Docker and where to find the Postman collection.

   

