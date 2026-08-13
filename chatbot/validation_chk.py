from flask import Flask, request, jsonify
from pydantic import BaseModel, EmailStr, ValidationError, field_validator
from typing import Optional

app = Flask(__name__)

class User(BaseModel):
    username: str
    email: EmailStr
    age: int

    @classmethod
    def validate_age(cls, age: int) -> int:
        if not (18 <= age <= 120):
            raise ValueError("Age must be between 18 and 120.")
        return age

    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, v):
        return v


@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Create a new user in the system. 

    This endpoint accepts a JSON object with the following fields:
    - username: A string representing the username.
    - email: A valid email address.
    - age: An integer representing the user's age (must be between 18 and 120).

    Returns:
    - 201: User created successfully
    - 400: Bad request if validations fail

    Example Request:
    {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "age": 25
    }

    Example Response (Success):
    {
        "message": "User created successfully."
    }

    Example Response (Validation Error):
    {
        "error": "Invalid input",
        "details": {
            "email": "value is not a valid email address"
        }
    }
    """
    try:
        user_data = request.json
        user = User(**user_data)
        return jsonify(message="User created successfully."), 201
    except ValidationError as e:
        return jsonify(error="Invalid input", details=e.errors()), 400
    except Exception as e:
        return jsonify(error="An unexpected error occurred", details=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True)