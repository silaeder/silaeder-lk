# Silaeder-lk

Портфолио Силаэдра

## Overview

This project is a portfolio application for Silaeder, featuring both an API service and a frontend.

- **API Service**: [https://api.silaeder.mrvasil.ru/](https://api.silaeder.mrvasil.ru/)
- **Frontend**: [https://silaeder.mrvasil.ru/](https://silaeder.mrvasil.ru/)

## Documentation

For detailed API documentation, please refer to [api_docs.md](api_docs.md).

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

To run the application using Docker Compose, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/silaeder-lk.git
   cd silaeder-lk
   ```

2. **Build and Run the Containers**

   Use Docker Compose to build and start the containers:

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker images and start the containers as defined in your `docker-compose.yml` file.

3. **Access the Application**

   - **API**: Access the API at [http://localhost:3750](http://localhost:3750) (or the port specified in your `docker-compose.yml`).

