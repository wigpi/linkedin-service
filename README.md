# LinkedIn API Service

This repository contains a FastAPI-based microservice that wraps the unofficial Python [linkedin-api](https://github.com/tomquirk/linkedin-api) to expose LinkedIn functionalities as RESTful endpoints. 

## Features

- **Search LinkedIn profiles** using a search string.
- **Retrieve detailed profile information** by URN ID.
- **Fetch contact information** for a LinkedIn profile.
- Automatically handles LinkedIn session management using cookies.

## Requirements

- Python >= 3.10
- Docker (optional, for containerized deployment)

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/linkedin-service.git
cd linkedin-service
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root with the following variables:

```env
LINKEDIN_USERNAME=your_linkedin_username
LINKEDIN_PASSWORD=your_linkedin_password
PORT=8000  # Optional, defaults to 8000
```

### 5. Run the Application

```bash
python main.py
```

The application will be available at `http://localhost:8000`.

### 6. Explore the API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Using Docker (Optional)

To run the application using Docker:

### 1. Build the Docker Image

```bash
docker build -t linkedin-service .
```

### 2. Run the Container

```bash
docker run --env-file .env -p 8000:8000 linkedin-service
```

The service will now be accessible at `http://localhost:8000`.

## Endpoints

### 1. **Search People**
   - **Endpoint**: `POST /search-people/`
   - **Request Body**:
     ```json
     {
       "search_string": "John Doe"
     }
     ```
   - **Response**:
     ```json
     {
       "results": [
         {
           "urn_id": "ACoAAB9835QBzIJrk2tHnszkUohH7xtAeY0RBlQ",
           "distance": "DISTANCE_1",
           "jobtitle": "Software Engineer",
           "location": "San Francisco, CA",
           "name": "John Doe"
         }
       ]
     }
     ```

### 2. **Get Profile Details**
   - **Endpoint**: `GET /profile-details/{urn_id}`
   - **Response**:
     ```json
     {
       "urn_id": "ACoAAB9835QBzIJrk2tHnszkUohH7xtAeY0RBlQ",
       "firstName": "John",
       "lastName": "Doe",
       "headline": "Software Engineer at LinkedIn",
       "locationName": "San Francisco, CA",
       "profile_pictures": {
         "img_100_100": "https://media.licdn.com/dms/image/...100_100",
         "img_200_200": "https://media.licdn.com/dms/image/...200_200"
       }
     }
     ```

### 3. **Get Profile Contact Info**
   - **Endpoint**: `GET /profile-contact-info/{urn_id}`
   - **Response**:
     ```json
     {
       "email_address": "johndoe@gmail.com",
       "phone_numbers": [{"type": "mobile", "number": "+123456789"}],
       "twitter_handles": ["@johndoe"],
       "websites": [{"url": "https://johndoe.com", "type": "personal"}],
       "address": "San Francisco, CA"
     }
     ```

## Development

### Running in Development Mode

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application with live reload:

```bash
uvicorn main:app --reload
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to suggest improvements or report bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This project uses an unofficial LinkedIn API library. Use it at your own risk, as it may violate LinkedIn’s terms of service. 