# Face Recognition System

## Introduction
This repository contains a face recognition system that utilizes state-of-the-art algorithms for detecting and recognizing human faces. This project is designed for scalability and ease of use across various applications.

## Installation Instructions
To set up the face recognition system, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/alexmontero2128/NenoIA.git
   ```

2. **Navigate to the Project Directory**
   ```bash
   cd NenoIA
   ```

3. **Install Dependencies**
   You can install the necessary dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**
   Update your database settings in the configuration file. Refer to `config/database.py` for parameters.

5. **Run the Application**
   Start the application using the following command:
   ```bash
   python app.py
   ```

## API Documentation
The API can be accessed at `/api/v1/recognize`. Below is an overview of the available endpoints:

- **POST /api/v1/recognize**
  - Description: Recognize faces from the uploaded image.
  - Request:
    - **Body**: Image file (multipart/form-data)
  - Response:
    - **200 OK**: A JSON object with recognition results.
    - **400 Bad Request**: If no file is provided or file type is invalid.

## Database Schema
The database schema for the face recognition system consists of the following tables:

### Users
- **id**: INT, Primary Key
- **name**: VARCHAR(100)
- **face_data**: BLOB

### Recognition Logs
- **id**: INT, Primary Key
- **user_id**: INT, Foreign Key
- **timestamp**: DATETIME
- **result**: JSON

## Security Considerations
- Ensure all sensitive data is encrypted in the database.
- Use HTTPS for all API communications.
- Regularly update dependencies to patch vulnerabilities.

## Future Enhancements
- Implement real-time recognition capabilities.
- Add support for additional authentication methods (e.g., two-factor authentication).
- Improve the user interface for better accessibility.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.