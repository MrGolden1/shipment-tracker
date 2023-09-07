# Project Documentation

Thank you for giving me this opportunity. Within this repository, you'll find all necessary components including the code base, documentation, sample data, tests, and resources needed to run the project.

## Note:
This task was experimental and not meant for production, therefore certain aspects haven't been implemented due to time constraints. For instance:
- The system doesn't have user-based capabilities nor authentication, hence the APIs are openly accessible.
- While there is a database design, there's no API, app, or procedure to manage them.
- Absence of Docker file or documentation for deploying on a production server.

## Technologies Used:
- Django
- Postgres
- Redis

## Setup & Running:
A Docker Compose file has been provided to streamline the setup and running of the project:

1. Create a `.env` file to set up the necessary variables. A `.env.example` file is available as a reference. However, I've included my own `.env` file to expedite the process. Put it in the root directory of the project.
2. Provide the necessary permissions to the entry script:
   ```
   sudo chmod +x entrypoint.sh
   ```
3. Build and start the services:
   ```
   docker-compose up
   ```
   Use `ctrl+c` to exit.
   
4. To import test data into the database, utilize the provided command:
   ```
   docker-compose run app python manage.py import_data sample_data.csv
   ```
   Enter 'y' when prompted.
   
5. Ensure the unit tests function correctly by executing:
   ```
   docker-compose run app python manage.py test
   ```
6. To run the application again, use:
   ```
   docker-compose up
   ```

## API Documentation:
API details can be found in the OpenAPI documentation located at `docs/swagger.yml`. For a quick reference:
- Endpoint for listing shipments: `http://127.0.0.1:8000/shipments`
- Endpoint to retrieve shipment details along with receiver's weather condition: `http://127.0.0.1:8000/shipments/DHL/TN12345678/`

## Tests:
Tests have been structured under the `shipments/tests` directory.

---

I eagerly await your feedback and am available to discuss any questions you may have.