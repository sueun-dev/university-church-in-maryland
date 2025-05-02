# University Church Web Application

This project is a Flask-based web application for University Church, designed to facilitate communication, resource sharing, and community engagement within the church community. It provides an easy-to-use platform with robust features tailored for both general users and administrators.
https://www.uchurchmd.org/
## Features

- **User Authentication**: Secure login system with built-in protection against excessive login attempts and brute-force attacks.
- **Content Management**: Admin users can easily create, read, update, and delete posts, facilitating seamless content dissemination.
- **File Management**: Securely upload, list, download, and delete various document types with enforced file validation.
- **Real-time Chat**: Integrated live chat functionality enabling real-time communication between users and administrators via WebSockets (Socket.IO).
- **RESTful API Endpoints**: Accessible JSON APIs for external integration and data retrieval of uploaded file information.
- **SEO and Accessibility**: Structured metadata, optimized page structures, and responsive designs for improved SEO and accessibility.

## Technologies Used

| Component            | Technology                             | Notes                                                   |
|----------------------|----------------------------------------|---------------------------------------------------------|
| Web Framework        | Flask                                  | Lightweight, flexible Python web framework              |
| Dependency Management| Poetry                                 | Simplified dependency management with built-in tooling  |
| Database             | SQLAlchemy (with Flask-Migrate)        | Robust ORM with easy schema migration capabilities      |
| Real-time Features   | Flask-SocketIO                         | Efficient WebSocket support for real-time communication |
| Cloud Platform       | Google Cloud Platform (GCP)            | Hosting via App Engine and Cloud SQL for databases      |
| Security             | Werkzeug Security, Flask sessions      | Secure password hashing, session handling, IP blocking  |
| Front-End            | Bootstrap, FontAwesome, Custom CSS     | Responsive UI with rich visual elements                 |
| Code Quality         | Black, flake8, isort                    | Automated formatting, linting, and import sorting       |
| Debugging            | Poetry built-in tools                  | Simplified debugging and dependency resolution          |

## Project Structure Overview

- `routes/`: Flask routes and view logic handling HTTP requests.
- `sockets/`: Handlers for managing real-time Socket.IO communications.
- `models.py`: Definition of database models (`PDFFile`, `Post`) using SQLAlchemy.
- `utils.py`: Utility functions for validation and general-purpose helpers.
- `config.py`: Centralized configuration management utilizing environment variables.
- `decorators.py`: Security and authentication decorators for route protection.
- `exceptions.py`: Custom exception handling for robust error management.
- `templates/`: HTML templates powered by Jinja2 templating engine.
- `static/`: CSS, JavaScript, and other static assets.
- `migration/`: Database migration scripts managed by Alembic.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account (App Engine and Cloud SQL)
- PostgreSQL/MySQL for Cloud SQL (recommended)
- Poetry (for dependency management)

### Installation

Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

Install dependencies using Poetry:
```bash
poetry install
```

Activate the Poetry virtual environment:
```bash
poetry shell
```

Set up environment variables:
```bash
cp .env.example .env
# Update .env with your actual environment variables
```

Initialize and migrate the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

Run the application locally:
```bash
flask run
```

## Deploying to Google Cloud Platform (GCP)

1. **Configure GCP**:
   - Create a new App Engine application in your GCP project.
   - Set up a Cloud SQL instance and configure it to connect with your Flask application.

2. **Deploy the application**:
   ```bash
   gcloud app deploy
   ```

3. **Monitoring & Logging**:
   - Utilize Google Cloud Monitoring and Logging to track application performance and troubleshoot issues.

## Contributing

Contributions are welcome and encouraged! Feel free to open issues for bugs, suggest improvements, or submit pull requests to enhance this project.

## License

This project is open source and freely available for personal or organizational use under the MIT License.

Developed by [Sueun Cho](https://github.com/sueun-dev).

---

_Last Updated: March 15, 2025_

