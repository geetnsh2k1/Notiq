# Notiq

Notiq is a real-time notification service built using FastAPI, WebSockets, Redis, and PostgreSQL. It is designed to deliver instant notifications to users with high scalability, reliability, and extensibility.

## Features

- **Real-Time Notifications:** Send real-time notifications to clients via WebSockets.
- **Asynchronous Processing:** Uses async I/O for non-blocking operations.
- **Redis Streams:** Leverages Redis Streams for message queuing and durability.
- **Database Persistence:** Data is stored in PostgreSQL with full CRUD support.
- **Extensible Architecture:** Modular components for channels, providers, templates, receivers, and requests.
- **Robust Error Handling:** Custom exception classes and centralized error handlers.
- **API Key Based Authentication:** Secure endpoints utilizing API keys and superuser verification.
- **Background Tasks:** Use of async tasks for non-blocking operations (e.g., sending notifications).

## Tech Stack

- **Python 3.9+**
- **FastAPI** for building the API server.
- **Redis** (using [redis-py asyncio](https://github.com/redis/redis-py)) for message streaming.
- **PostgreSQL** as the primary relational database.
- **SQLAlchemy 2.0+** for database ORM.
- **Alembic** for migrations.
- **Uvicorn** as the ASGI server.

## Project Structure

```
notification/
├── alembic/                  # Database migration scripts
├── config/                   # Configuration files (base and environment-specific configs)
├── controller/               # API endpoints
├── db/                       # Database setup and models
├── exception/                # Custom application and database exceptions
├── enums/                    # Enumerations (e.g. notification types, statuses)
├── logger/                   # Logging configuration and middleware
├── mappers/                  # DTO (Data Transfer Object) mappings
├── models/                   # Database models
├── redis_client/             # Redis configuration and client
├── repository/               # Data access objects (DAO) for CRUD operations
├── schema/                   # Pydantic models for request/response validation
├── utils/                    # Utility modules (helpers, exception handler, security, etc.)
├── .env                      # Environment variable definitions
├── alembic.ini               # Alembic configuration
├── requirements.txt          # Python dependencies
└── main.py                   # Entry point of the application
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/notiq.git
   cd notiq
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configuration:**

   - The application uses configuration files in the `config/` directory. A default configuration is provided in `config/base.ini` and environment-specific overrides in `config/local/application.ini`.
   - Copy or adjust the `.env` file to set your environment. For example:

     ```env
     APP_ENV=local
     ```

4. **Database setup:**

   - Ensure PostgreSQL is installed and running.
   - Update the `config/local/application.ini` file under the `[DATABASE]` section with your database credentials.
   - Run Alembic migrations to set up the database schema:

     ```bash
     alembic upgrade head
     ```

5. **Redis setup:**

   - Ensure Redis is installed and running.
   - Update the `[REDIS]` section in your config file with the appropriate connection details.

## Running the Service

Start the application using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The service will be available at `http://localhost:8000`. API documentation is available at `/docs` (Swagger UI) and `/redoc`.

## API Endpoints

The API endpoints are organized into several modules:

- **Client:** Create clients, regenerate API keys, and mark clients inactive.
- **Channel:** Create and manage channels.
- **Provider:** Create and manage notification providers.
- **Receiver:** Manage receiver details.
- **Template:** Create and update notification templates.
- **Notification:** Send notifications to users.
- **WebSocket:** Connect to the notification stream via WebSocket.

For a complete list of endpoints with details, refer to the automatically generated OpenAPI docs at `/openapi.json` or the Swagger UI at `/docs`.

## Logging & Error Handling

- **Logging:** Logging is configured using the Python logging module and loaded from the configuration files. Custom middleware ensures that every request is logged with a unique request ID.
- **Error Handling:** Custom exceptions (`AppException`, `DBException`, etc.) are defined and globally handled using exception handlers in `utils/exception_handler.py`.

## Contributing

Contributions are welcome! Please open issues or submit PRs for bugs, feature requests, or any improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
