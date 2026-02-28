# CDC Export System (High-Performance User Data)

A production-ready Change Data Capture (CDC) system built to stream
incremental updates from a PostgreSQL database into CSV format using a
Watermarking synchronization strategy.

------------------------------------------------------------------------

## Features

-   **Incremental CDC Logic**: Only exports new or updated records since
    the last sync.
-   **Watermarking System**: Tracks state per `consumer_id` to prevent
    data duplication.
-   **Scalability**: Optimized to handle 100,000+ records efficiently.
-   **Containerized**: Fully orchestrated with Docker and Docker
    Compose.
-   **Production-Ready**: Includes logging, health checks, and automated
    test coverage.

------------------------------------------------------------------------

## Getting Started

### 1️ Clone the Repository

``` bash
git clone https://github.com/sindhutej-6/CDC_Export_System
cd CDC_Export_System
```

### 2️ Environment Configuration

Create a `.env` file from the provided example:

``` bash
cp .env.example .env
```

### 3️ Launch the Application

Start the API and Database with a single command:

``` bash
docker-compose up --build -d
```

### 4️ Seed the Database

Generate 100,000 mock user records to test high-volume export:

``` bash
docker-compose exec app python seeds/seed.py
```

------------------------------------------------------------------------

##  API Endpoints

  --------------------------------------------------------------------------
  Method             Endpoint                  Description
  ------------------ ------------------------- -----------------------------
  GET                `/health`                 Returns system status and
                                               current timestamp

  POST               `/export/{consumer_id}`   Triggers an incremental CSV
                                               export for a specific client
  --------------------------------------------------------------------------

------------------------------------------------------------------------

##  Automated Testing

Run the integration and unit test suite inside the container:

``` bash
docker-compose exec app python -m pytest tests/
```

------------------------------------------------------------------------

##  Project Structure

    app/        → FastAPI routes, SQLAlchemy models, and CDC services
    tests/      → Automated test suite for API and logic verification
    seeds/      → SQL initialization and Python data generation scripts
    output/     → Local directory where generated CSV exports are stored

------------------------------------------------------------------------
