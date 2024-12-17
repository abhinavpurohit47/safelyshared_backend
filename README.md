## Project Description

The Safely Shared Backend is a Django-based application designed to provide secure file upload, download, and encryption services. This project ensures that files are encrypted before being stored and decrypted upon download, maintaining the confidentiality and integrity of the data.

## Tech Stack

- **Backend Framework**: Django
- **Database**: PostgreSQL (or any other database supported by Django)
- **Containerization**: Docker, Docker Compose
- **Encryption**: AES (Advanced Encryption Standard)

## Features
- **User Management**: User registration, authentication, and authorization to ensure that only authorized users can access and manage files.
- **Secure File Upload**: Users can upload files which are encrypted before storage.
- **Secure File Download**: Files are decrypted upon download to ensure data security.
- **Temporary Download Links**: Generate secure, temporary download links for sharing files.
- **File Management**: List and delete uploaded files securely.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd safely-shared-backend
    ```
2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Apply the migrations:
    ```sh
    python manage.py migrate
    ```

4. Run the development server:
    ```sh
    python manage.py runserver
    ```
you can also run : docker-compose up --build

for generating AES KEY: python3 manage.py generate_key
## Usage

1. Access the web application:
    Open your web browser and navigate to `http://localhost:8000`.

2. Use the provided endpoints to upload, download, and manage files securely.

## How It Is Useful

- **Data Security**: Ensures that sensitive files are encrypted and secure during storage and transmission.
- **Ease of Use**: Provides a simple interface for uploading and downloading files.
- **Temporary Access**: Allows generating temporary download links for secure file sharing.
- **User Management**: Ensures that only registered and authenticated users can access and manage files, enhancing security.
