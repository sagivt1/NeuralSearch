# Neural Search

A full-stack application demonstrating a powerful neural search engine. It uses vector embeddings to find items based on natural language queries, powered by a Python backend, a PostgreSQL database with pgvector, and an interactive Streamlit frontend.

## Table of Contents

- [Features](#features)
- [🛠️ Dependencies & Prerequisites](#️-dependencies--prerequisites)
- [⚙️ Installation & Setup](#️-installation--setup)
- [▶️ Running the Project](#️-running-the-project)
- [📜 License](#-license)

## Features

*   **Vector-Based Search API**: A FastAPI backend that converts text queries into vector embeddings to find the most semantically similar results.
*   **Background Task Processing**: Utilizes Celery and Redis for handling computationally intensive tasks, like data embedding, without blocking the API.
*   **Interactive Web UI**: A Streamlit frontend provides a user-friendly interface to interact with the search engine.
*   **Containerized Environment**: The entire application stack is managed with Docker and Docker Compose for consistent, one-command setup and deployment.
*   **Efficient Package Management**: Uses `uv` for fast and reliable Python package management.

## 🛠️ Dependencies & Prerequisites

You must have Docker and Docker Compose installed on your local machine. These tools are required to build and run the containerized application services.

*   **Docker Engine**: The underlying containerization platform.
*   **Docker Compose**: The tool for defining and running multi-container Docker applications.

Follow the official instructions for your operating system to install them:

*   **macOS**: Install Docker Desktop for Mac.
*   **Windows**: Install Docker Desktop for Windows.
*   **Linux**: Install the Docker Engine and then the Docker Compose Plugin.

## ⚙️ Installation & Setup

Follow these steps to get your local development environment set up and running.

### 1. Clone the Repository

First, clone the project repository to your local machine.

```bash
git clone https://github.com/sagivt1/NeuralSearch.git
cd NeuralSearch
```

### 2. Configure Environment Variables

The application uses a `.env` file to manage secrets and configuration for the database. Create a `.env` file in the root of the project by copying the example file.

```bash
# This command works on Linux and macOS
cp .env.example .env
```

If you are on Windows, you can manually create a file named `.env` and copy the contents from `.env.example`.

The default values in `.env.example` are suitable for local development. Your `.env` file should contain the following, which are used by the `db` service in `docker-compose.yml`:

```env
# .env

# PostgreSQL Database Credentials
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=neuralsearch
```

**Note:** The `docker-compose.yml` file automatically constructs and provides the full `DATABASE_URL` and `REDIS_URL` to the application containers. You do not need to set them in the `.env` file.

## ▶️ Running the Project

The entire application stack is managed by Docker Compose. The commands below should be run from the root of the project directory.

### Development Mode

This command starts all services (API, worker, database, frontend) in detached mode. The API service is configured with hot-reloading, so changes to the source code will automatically restart the server.

```bash
docker-compose up -d
```

To view the logs from all running services, you can run:

```bash
docker-compose logs -f
```

Once the containers are running, you can access the services at the following URLs:

*   **API (FastAPI)**: http://localhost:8000
*   **Frontend (Streamlit)**: http://localhost:8501

### Production Mode

To build and run the containers for a production-like environment, use the `--build` flag. This ensures the Docker images are rebuilt with the latest code. The `api` service in the provided `docker-compose.yml` includes `--reload`, which is ideal for development. For a true production deployment, you would typically remove the `command` override from the `api` service in `docker-compose.yml` to use the production `CMD` from the `Dockerfile`.

```bash
docker-compose up -d --build
```

### Stopping the Application

To stop the running services without removing them, use the `stop` command as specified.

```bash
docker-compose stop
```

To stop and remove all containers, networks, and volumes created by `docker-compose up`, run:

```bash
docker-compose down
```

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
