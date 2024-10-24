# API Documentation

This document provides detailed information about the available API endpoints for the project. Each section describes a specific route, its purpose, required parameters, and expected responses.

## Table of Contents

1. [Authentication Routes](#authentication-routes)
2. [User Routes](#user-routes)
3. [Project Routes](#project-routes)
4. [Guild Routes](#guild-routes)

## Authentication Routes

### Login

Authenticates a user and returns a JWT token.

- **URL:** `/auth/login`
- **Method:** GET
- **URL Params:** 
  - `login=[string]`
  - `password=[string]`
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "success": true,
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
- **Error Response:**
  - **Code:** 400
  - **Content:**
    ```json
    {
      "error": "Login and password are required"
    }
    ```
  OR
  - **Code:** 401
  - **Content:**
    ```json
    {
      "success": false
    }
    ```

### Authentication Errors

For all routes that require authentication (marked with "Auth Required: Yes"), the following error responses may occur if there are issues with the provided JWT token:

1. Invalid Token

- **Code:** 401
- **Content:**
  ```json
  {
    "message": "Token is invalid!",
    "error": "<error_details>"
  }
  ```

This error occurs when the provided token is not properly formatted or has been tampered with.

2. Expired Token

- **Code:** 401
- **Content:**
  ```json
  {
    "message": "Token is expired!"
  }
  ```

This error occurs when the provided token has exceeded its expiration time.

To avoid these errors, ensure that you're using a valid, non-expired JWT token in the Authorization header of your requests.



Note: All routes marked with "Auth Required: Yes" need to include the JWT token in the Authorization header of the request. The format should be:

```
Authorization: <JWT_TOKEN>
```

### Get Username

Retrieves the username associated with the provided JWT token.

- **URL:** `/auth/get_username`
- **Method:** GET
- **Auth Required:** Yes
- **Headers:**
  - `Authorization: <JWT_TOKEN>`
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "username": "John Doe"
    }
    ```
- **Error Response:**
  - **Code:** 401
  - **Content:**
    ```json
    {
      "message": "Token is missing!"
    }
    ```
  OR
  - **Code:** 401
  - **Content:**
    ```json
    {
      "message": "Token is invalid!",
      "error": "<error_details>"
    }
    ```
  OR
  - **Code:** 401
  - **Content:**
    ```json
    {
      "message": "Token is expired!"
    }
    ```
  OR
  - **Code:** 404
  - **Content:**
    ```json
    {
      "error": "User not found"
    }
    ```

This endpoint allows clients to retrieve the username associated with a valid JWT token. It's useful for displaying the current user's name in the application interface.

## User Routes


### Get All Users

Retrieves all users.

- **URL:** `/user/get_all_users`
- **Method:** GET
- **Auth Required:** Yes
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "user_id": {
        "login": "john.dd",
        "email": "john@example.com",
        "full_name": "John Doe",
        "birth_date": "1990-01-01",
        "photo_path": "/path/to/photo.jpg",
        "contacts": "Contact info",
        "interests": "Interests",
        "is_admin": false
      }
    }
    ```

### Add User

Adds a new user to the database.

- **URL:** `/user/add_user`
- **Method:** POST
- **Auth Required:** Yes
- **Request Body:**
  ```json
  {
    "real_name": "John Doe"
  }
  ```
- **Success Response:**
  - **Code:** 201
  - **Content:**
    ```json
    {
      "success": true,
      "username": "john.dd",
      "password": "randompassword"
    }
    ```
- **Error Response:**
  - **Code:** 400
  - **Content:**
    ```json
    {
      "error": "Real name is required"
    }
    ```

### Get User

Retrieves user information by email or login.

- **URL:** `/user/get_user`
- **Method:** GET
- **Auth Required:** Yes
- **URL Params:** 
  - `email_or_login=[string]`
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "user": {
        "user_id": 1,
        "login": "john.dd",
        "email": "john@example.com",
        "full_name": "John Doe",
        "birth_date": "1990-01-01",
        "photo_path": "/path/to/photo.jpg",
        "contacts": "Contact info",
        "interests": "Interests",
        "is_admin": false
      }
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "error": "User not found"
    }
    ```

### Update User

Updates user information.

- **URL:** `/user/update_user`
- **Method:** POST
- **Auth Required:** Yes
- **Request Body:**
  ```json
  {
    "email_or_login": "john.dd",
    "updates": {
      "full_name": "John Doe Jr.",
      "birth_date": "1990-02-01"
    }
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "success": true
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "error": "User not found or update failed"
    }
    ```

### Delete User

Deletes a user from the database.

- **URL:** `/user/delete_user`
- **Method:** DELETE
- **Auth Required:** Yes
- **URL Params:** 
  - `email_or_login=[string]`
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "success": true
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "error": "User not found"
    }
    ```

### Add Class

Adds multiple users to the database at once.

- **URL:** `/user/add_class`
- **Method:** POST
- **Auth Required:** Yes
- **Request Body:**
  ```json
  {
    "users": [
      {
        "real_name": "John Doe"
      },
      {
        "real_name": "Jane Smith"
      }
    ]
  }
  ```
- **Success Response:**
  - **Code:** 201
  - **Content:**
    ```json
    {
      "success": true,
      "added_users": [
        {
          "username": "john.dd",
          "password": "randompassword1"
        },
        {
          "username": "jane.ss",
          "password": "randompassword2"
        }
      ]
    }
    ```
- **Error Response:**
  - **Code:** 400
  - **Content:**
    ```json
    {
      "error": "Real name is required for all users. Missing for: {user_info}"
    }
    ```

## Project Routes

### Get All Projects

Retrieves all projects.

- **URL:** `/projects/get_all_projects`
- **Method:** GET
- **Auth Required:** Yes
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "project_id": {
        "title": "Project Title",
        "description": "Project Description",
        "teacher": "teacher.login",
        "team": ["john.dd", "jane.ss"],
        "status": "In Progress",
        "short_description": "Short Description",
        "video_link": "https://example.com/video",
        "presentation_path": "/path/to/presentation.pdf"
      }
    }
    ```
### Get Project Members

Retrieves the members of a specific project.

- **URL:** `/projects/get_project_members`
- **Method:** GET
- **Auth Required:** Yes
- **URL Params:** 
  - `project_id=[integer]`
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "projects": [
        {
          "user_id": 1,
          "login": "john.dd",
          "full_name": "John Doe"
        },
        {
          "user_id": 2,
          "login": "jane.ss",
          "full_name": "Jane Smith"
        }
      ]
    }
    ```
- **Error Response:**
  - **Code:** 400
  - **Content:**
    ```json
    {
      "message": "Project ID is required"
    }
    ```

### Get Project

Retrieves information about a specific project.

- **URL:** `/projects/get_project`
- **Method:** GET
- **Auth Required:** Yes
- **URL Params:** 
  - `project_id=[integer]`
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "project_id": 1,
      "title": "Project Title",
      "description": "Project Description",
      "teacher": "teacher.login",
      "team": ["john.dd", "jane.ss"],
      "status": "In Progress",
      "video_link": "https://example.com/video",
      "presentation_path": "/path/to/presentation.pdf"
    }
    ```
- **Error Response:**
  - **Code:** 400
  - **Content:**
    ```json
    {
      "message": "Project ID is required"
    }
    ```

### Get Projects by User

Retrieves all projects associated with a specific user.

- **URL:** `/projects/get_projects_by_user`
- **Method:** GET
- **Auth Required:** Yes
- **URL Params:** 
  - `login=[string]`
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    [
      {
        "project_id": 1,
        "title": "Project 1",
        "description": "Description 1"
      },
      {
        "project_id": 2,
        "title": "Project 2",
        "description": "Description 2"
      }
    ]
    ```
- **Error Response:**
  - **Code:** 400
  - **Content:**
    ```json
    {
      "message": "Login is required"
    }
    ```

### Create Project

Creates a new project.

- **URL:** `/projects/create`
- **Method:** POST
- **Auth Required:** Yes
- **Request Body:**
  ```json
  {
    "title": "New Project",
    "description": "Project Description",
    "short_description": "Short Description",
    "teacher": "teacher.login",
    "team": ["john.dd", "jane.ss"],
    "status": "New"
  }
  ```
- **Success Response:**
  - **Code:** 201
  - **Content:**
    ```json
    {
      "message": "Project created"
    }
    ```
- **Error Response:**
  - **Code:** 400
  - **Content:**
    ```json
    {
      "message": "Field {field_name} is required"
    }
    ```

### Update Project

Updates an existing project.

- **URL:** `/projects/update/<int:project_id>`
- **Method:** POST
- **Auth Required:** Yes
- **Request Body:**
  ```json
  {
    "title": "Updated Project Title",
    "description": "Updated Description",
    "team": ["john.dd", "jane.ss", "new.user"]
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "Project updated"
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "message": "Project not found"
    }
    ```

### Add User to Project

Adds a user to an existing project.

- **URL:** `/projects/add_user/<int:project_id>`
- **Method:** POST
- **Auth Required:** Yes
- **Request Body:**
  ```json
  {
    "login": "new.user"
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "User added to project"
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "message": "Project {project_id} not found"
    }
    ```

### Remove User from Project

Removes a user from an existing project.

- **URL:** `/projects/remove_user/<int:project_id>`
- **Method:** POST
- **Auth Required:** Yes
- **Request Body:**
  ```json
  {
    "login": "user.to.remove"
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "User removed from project"
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "message": "Project {project_id} not found"
    }
    ```

### Delete Project

Deletes an existing project.

- **URL:** `/projects/delete/<int:project_id>`
- **Method:** POST
- **Auth Required:** Yes
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "Project deleted"
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "message": "Project not found"
    }
    ```

## Guild Routes

### Create Guild

Creates a new guild.

- **URL:** `/guild/create`
- **Method:** POST
- **Auth Required:** Yes
- **Request Body:**
  ```json
  {
    "title": "New Guild",
    "guild_team": ["user1.login", "user2.login"]
  }
  ```
- **Success Response:**
  - **Code:** 201
  - **Content:**
    ```json
    {
      "message": "Guild created",
      "guild_id": 1,
      "title": "New Guild",
      "members": ["user1.login", "user2.login"]
    }
    ```
- **Error Response:**
  - **Code:** 400
  - **Content:**
    ```json
    {
      "message": "Some users do not exist",
      "missing_users": ["nonexistent.user"]
    }
    ```

### Get Guild

Retrieves information about a specific guild.

- **URL:** `/guild/get_guild`
- **Method:** GET
- **Auth Required:** Yes
- **URL Params:** 
  - `guild_id=[integer]`
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "guild_id": 1,
      "title": "Guild Title",
      "guild_team": "user1.login,user2.login"
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "message": "Guild not found"
    }
    ```

### Add User to Guild

Adds a user to an existing guild.

- **URL:** `/guild/add_user/<int:guild_id>`
- **Method:** POST
- **Auth Required:** Yes
- **Request Body:**
  ```json
  {
    "login": "new.user"
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "User added to guild"
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "message": "Guild not found"
    }
    ```

### Update Guild

Updates an existing guild.

- **URL:** `/guild/update/<int:guild_id>`
- **Method:** POST
- **Auth Required:** Yes
- **Request Body:**
  ```json
  {
    "title": "Updated Guild Title",
    "guild_team": ["user1.login", "user2.login", "new.user"]
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "Guild updated successfully",
      "guild_id": 1,
      "title": "Updated Guild Title",
      "members": ["user1.login", "user2.login", "new.user"]
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "message": "Guild not found"
    }
    ```

### Remove User from Guild

Removes a user from an existing guild.

- **URL:** `/guild/remove_user/<int:guild_id>`
- **Method:** POST
- **Auth Required:** Yes
- **Request Body:**
  ```json
  {
    "login": "user.to.remove"
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "User removed from guild"
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "message": "Guild not found"
    }
    ```

### Delete Guild

Deletes an existing guild.

- **URL:** `/guild/delete/<int:guild_id>`
- **Method:** DELETE
- **Auth Required:** Yes
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "Guild deleted successfully"
    }
    ```
- **Error Response:**
  - **Code:** 404
  - **Content:**
    ```json
    {
      "message": "Guild not found"
    }
    ```



This documentation covers the main routes and their functionalities. Make sure to handle errors appropriately and validate input data on the server-side for security purposes.
