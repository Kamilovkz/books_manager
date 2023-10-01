# My Book Manager

Welcome to My Book Manager! This application helps you manage your book collection.

## Installation

Before running the project, follow these steps:

1. Create an `.env` file based on the provided `.envsample` file.

    ```env
    # Database settings
    DATABASE_URL=postgres://db_user:db_password@db_host:db_port/db_name

    # RabbitMQ settings
    RABBITMQ_DEFAULT_USER=guest
    RABBITMQ_DEFAULT_PASS=guest
    ```

2. Build and run the project using Docker Compose:

    ```bash
    docker compose build && docker compose up -d
    ```

## API URLs

You can access the API documentation by visiting [localhost:8000/swagger](http://localhost:8000/swagger). The main endpoints for managing books are as follows:

- List All Books: `GET /api/books/`
- Filter by Date: `GET /api/books/?from={from_date}&to={to_date}`
- View Book Details: `GET /api/books/?book_id={book_id}`
- Add Book to Favorites: `POST /api/books/favorite/`
- Remove Book from Favorites: `DELETE /api/books/favorite/`

### Admin Credentials (for testing)

- Email: `admin@admin.com`
- Password: `admin`

## Frontend Commands

To interact with the API, here are some basic commands:

1. **List All Books**: View the list of all books in your collection.
2. **Filter by Date**: Filter books by publication date using the "From" and "To" date inputs and clicking the "Filter" button.
3. **View Book Details**: Click on a book title to view its details.
4. **Add to Favorites**: Add a book to your favorites by clicking the "Add to Favorites" button.
5. **Remove from Favorites**: Remove a book from your favorites by clicking the "Remove from Favorites" button.

## Email Verification

Please note that email verification logic is not implemented in this project. You can adapt and implement this feature according to your requirements.

Happy reading!
