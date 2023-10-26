# Book Web Service (BWS) 

API service for providing the user with access to various literary works.  
**Stack**: Python, Aiohttp, PostgreSQL, SQLAlchemy

## Getting Started

### Prerequisites
- [MinIO](https://min.io/) - You need to have MinIO up.
- [PostgreSQL](https://www.postgresql.org/) - You need to have PostgreSQL up.

### Service
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
- Clone the repository
 - Use [poetry](https://python-poetry.org/) to install dependencies:

   ```sh
   poetry install
   ```
 - Create or use existing `.env` file in the `/environment` directory of the project.  
   Set environment variables from `.env` file:
   ```sh
   set -a && source environment/local.env && set +a
   ```
 - Make migrations for consistency database:
   ```sh
    python src/manage.py migrate
   ```
 - Start service :
   ```sh
    python src/manage.py start
   ```

## Running in Docker

### Dockerfile
1. Build the Docker image:
   ```sh
   docker build -t bws_app .
   ```
2. Run the Docker container:
   ```sh
   docker run -p 8080:8080 --env-file environment/local.env bws_app
   ```

### Docker-compose
1. Start all side-app containers
   ```sh
   docker-compose up
   ```

## Endpoints (`/api/docs`):

- Route: `/readiness`  
Description: This endpoint is used to check the readiness of the API.


- Route: GET `/liveness`  
Description: This endpoint is used to check the liveness of the API.



- Route: GET | POST `/api/v1/books`  
Description: This endpoint is used to retrieve and send information about books.


- Route: GET `/api/v1/book_files/{id}`  
Description: This endpoint is used to download files associated with a specific book.


- Route: POST `/api/v1/book_files/{id}`  
Description: This endpoint is used to upload files associated with a specific book.

## Running the tests (***experimental!***)
   **Tests are not ready yet for running in such a way!**

  - Edit environment variables in `tests/conftest.py`
  - Run tests
    ```sh
    pytest .
    ```

## TODO

- [ ] Write connection with S3 in async way
- [ ] Add fixtures for integrity tests
- [ ] CI/CD. Write a pipeline for automated testing and code quality checks
- [x] CI/CD. Write a pipeline for quality checks (flake8, mypy)
- [ ] Set up logging in better way

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Author 1** - *Initial work* - [Author1](https://github.com/author1)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

