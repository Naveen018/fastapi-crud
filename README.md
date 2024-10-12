# FastAPI CRUD Application

This project implements a FastAPI application that performs CRUD operations for Items and User Clock-In Records using MongoDB.


## Setup and Running Locally

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fastapi-crud.git
   cd fastapi-crud-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up a MongoDB database (locally or using MongoDB Atlas) and update the connection string in `app/database.py`.
(I have used MongoDB Atlas for db connection)

5. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

6. Access the API documentation at `http://localhost:8000/docs`.

## API Endpoints

### Items

- POST /items/: Create a new item
- GET /items/{item_id}: Retrieve an item by ID
- GET /items/filter: Filter items based on email, expiry date, insert date, and quantity
- GET /items/aggregate: Aggregate data to return the count of items for each email
- DELETE /items/{item_id}: Delete an item based on its ID
- PUT /items/{item_id}: Update an item's details by ID

### Clock-In Records

- POST /clock-in/: Create a new clock-in entry
- GET /clock-in/{clock_in_id}: Retrieve a clock-in record by ID
- GET /clock-in/filter: Filter clock-in records based on email, location, and insert datetime
- DELETE /clock-in/{clock_in_id}: Delete a clock-in record based on its ID
- PUT /clock-in/{clock_in_id}: Update a clock-in record by ID

## Hosted Application

The application is hosted on [Koyeb/Heroku/etc.]. You can access the Swagger documentation at:

[Insert Swagger URL here once deployed]

## Technologies Used

- FastAPI
- MongoDB (with Motor for async operations)
- Pydantic for data validation
- Uvicorn as the ASGI server
