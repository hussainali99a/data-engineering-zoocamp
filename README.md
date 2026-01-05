# Data Engineering ZooCamp

A data engineering workshop project demonstrating data pipeline development, containerization, and database ingestion using modern tools and practices.

## Overview

This repository contains a complete data pipeline for processing NYC Yellow Taxi Trip Records. It showcases:
- **Data Ingestion**: Automated download and ingestion of NYC taxi data into PostgreSQL
- **Containerization**: Docker-based deployment for reproducibility and scalability
- **Database Management**: PostgreSQL setup with PgAdmin for data exploration
- **Python Data Processing**: Pandas-based ETL operations with SQLAlchemy ORM

## Technology Stack

- **Python 3.13**: Modern Python for data processing
- **PostgreSQL 18**: Robust relational database
- **Docker & Docker Compose**: Containerization and orchestration
- **SQLAlchemy**: SQL toolkit and ORM
- **Pandas**: Data manipulation and analysis
- **Click**: Command-line interface creation
- **PyArrow**: Efficient data serialization

## Project Structure

```
├── README.md                    # This file
├── pipeline/                    # Main application directory
│   ├── main.py                 # Entry point placeholder
│   ├── pipeline.py             # Data pipeline logic
│   ├── ingest_data.py          # NYC taxi data ingestion script
│   ├── Dockerfile              # Docker container definition
│   ├── docker-compose.yaml     # Multi-container orchestration
│   ├── Notebook.ipynb          # Jupyter notebook for exploration
│   ├── pyproject.toml          # Python project configuration
│   ├── README.md               # Pipeline-specific documentation
│   └── ny_taxi_postgres_data/  # PostgreSQL data volume
├── test/                       # Test directory
└── .git/                       # Git version control
```

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Python 3.13+ (for local development)
- Git

### 1. Start the Database Services

```bash
cd pipeline
docker-compose up -d
```

This starts:
- **PostgreSQL database** (port 5432)
- **PgAdmin web interface** (port 8085)

### 2. Run the Data Ingestion Pipeline

Using Docker:
```bash
docker build -t ny-taxi-pipeline .
docker run --network host \
  -e PG_USER=root \
  -e PG_PASS=root \
  -e PG_HOST=localhost \
  -e PG_DB=ny_taxi \
  ny-taxi-pipeline \
  --year 2021 --month 1
```

Or with Python directly (after installing dependencies):
```bash
pip install -e .
python ingest_data.py --year 2021 --month 1 --pg-user root --pg-pass root --pg-host localhost --pg-db ny_taxi
```

### 3. Access PgAdmin

- **URL**: http://localhost:8085
- **Email**: admin@admin.com
- **Password**: root

## Configuration

### Data Ingestion Options

The `ingest_data.py` script supports the following command-line options:

- `--pg-user`: PostgreSQL username (default: `root`)
- `--pg-pass`: PostgreSQL password (default: `root`)
- `--pg-host`: PostgreSQL host (default: `localhost`)
- `--pg-port`: PostgreSQL port (default: `5432`)
- `--pg-db`: PostgreSQL database (default: `ny_taxi`)
- `--year`: Year of taxi data to ingest (default: `2021`)
- `--month`: Month of taxi data to ingest (default: `1`)
- `--chunksize`: Number of rows per chunk (default: `100000`)
- `--target-table`: Target table name (default: `yellow_taxi_data`)

### Supported Data Format

The pipeline processes NYC Yellow Taxi data with the following columns:
- VendorID, passenger_count, trip_distance, RatecodeID
- store_and_fwd_flag, PULocationID, DOLocationID
- payment_type, fare_amount, extra, mta_tax
- tip_amount, tolls_amount, improvement_surcharge
- total_amount, congestion_surcharge
- tpep_pickup_datetime, tpep_dropoff_datetime

## Architecture

### Docker Composition

```yaml
Services:
├── pgdatabase    - PostgreSQL 18 (persistent storage)
└── pgadmin       - PgAdmin 4 (database management UI)

Volumes:
├── ny_taxi_postgres_data  - Database persistence
└── pgadmin_data           - PgAdmin configuration persistence
```

### Docker Image

The Docker image:
1. Uses Python 3.13 slim base image
2. Installs `uv` for fast dependency management
3. Syncs dependencies from lock file (reproducible builds)
4. Runs `ingest_data.py` as the entry point

## Development

### Installing Dependencies

```bash
pip install -e ".[dev]"
```

This installs:
- **Runtime**: click, pandas, psycopg2-binary, pyarrow, sqlalchemy, tqdm
- **Development**: jupyter, pgcli

### Running Locally

```bash
python ingest_data.py --help
```

### Jupyter Notebook

Interactive exploration is available in `Notebook.ipynb`:

```bash
jupyter notebook Notebook.ipynb
```

## Data Source

Taxi data is sourced from the [NYC Taxi and Limousine Commission](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) via the DataTalks Club repository.

## What is Docker?

Docker is a containerization platform that isolates applications in lightweight, reproducible environments. Key benefits:

- **Consistency**: "Works on my machine" becomes "Works everywhere"
- **Scalability**: Deploy to cloud providers (AWS, GCP, Azure) with minimal changes
- **Efficiency**: Lighter than virtual machines, faster startup times
- **Version Control**: Docker images can be versioned and tracked

This project demonstrates Docker's power by allowing the entire data pipeline to run identically on any system.

## Troubleshooting

### Port Already in Use
If ports 5432 or 8085 are in use:
```bash
# Stop existing containers
docker-compose down

# Or use different ports in docker-compose.yaml
```

### Connection Refused
Ensure PostgreSQL is fully initialized before running the pipeline:
```bash
docker-compose logs pgdatabase
```

### Permission Errors
Run Docker commands with appropriate permissions or add your user to the docker group.

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This is a workshop project for educational purposes.

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/)
- [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)

