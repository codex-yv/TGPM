### Overview:
- API request authentication required for Private APIs(Production).
- In this code the database operations are currently synchronus which can be updated to Ansynchronus

- Currently images are being stored inside the database as `BYTEA` we can use cloud storage services like *Cloudinary* (easy to setup) to store image and use store URL in our database.

- Image of `REDIS` is added and configured in the codebase, which can be implemented in future.

- Currently the packages are being returned all at a time, which will increase in loading time. We can optimize it to return packages as segments.


***NOTE :*** All the above mentioned optimization can be implemented with in few more days of development.

### Setup:

- Create an `.env` file with variables:
    ```bash
    POSTGRES_URL = "postgresql://postgres:postgres@localhost:5432/tirthghumoPackage"
    
    REDIS_URL = "redis://localhost:6379"
    ```

- Install the `Dependencies`. Run the below command in root dir:
    ```bash
    pip install -r requirements.txt
    ```
- Install `Postgres` and `Redis` image. Run the below command in root dir:

    ```bash
    docker compose up -d
    ```
    ***Note:*** Make sure you have docker installed and configured.

- `Optional:` Run the below command in PowerShell to run Postgress commands.
    ```bash
    docker exec -it tirthghumo-postgres psql -U postgres -d tirthghumoPackage
    ```


***Note:*** The above application is built and tested on `Windows`.