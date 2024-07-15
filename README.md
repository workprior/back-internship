# back-internship
add commit
=======
# My FastAPI Project

Here are the instructions on how to run this project locally.

## Installation

### 1. Clone the repositoryasd

Clone this repository to your local environment:

```bash
git clone https://github.com/workprior/back-internship.git
cd back-internship
```

### 2. Installing Poetry

On Windows (Powershell)

```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```
Check version

```bash
poetry -V
```
### 3. Setting Up the Project

#### 3.1 Initialize the Virtual Environment and Install Dependencies

Run the following command to create the virtual environment and install all dependencies specified in the pyproject.toml file:

```bash
poetry install
```
#### 3.2 Activate the Virtual Environment

Activate the virtual environment created by Poetry:

```bash
poetry shell
```
#### 3.3 Running the application

Start the development server:
```bash
uvicorn app.main:app --reload
```
The web application will be available at 'http://127.0.0.1:8000'.

#### 3.4 Testing

To run tests, use pytest:
```bash
pytest
```

### 4. Using Docker

Install Docker Engine from official web-site https://docs.docker.com/engine/install/d

Check version

```bash
docker -v
```
#### 4.1 Build and run the Docker containers

Run the following command to build and start the Docker containers:

```bash
docker-compose up --build

```

#### 4.2 Access the FastAPI application

Once the containers are up and running, you can access the FastAPI application at url:

```bash
http://localhost:8000
```

#### 4.3 Check database connections

You can use the following endpoints to check the connections to PostgreSQL and Redis:

Check PostgreSQL connection:

```bash
http://localhost:8000/check-postgres

```

Check Redis connection:

```bash
http://localhost:8000/check-redis
```


### 4. Init migrations
To create a new migration, use the following command:

 ```bash
alembic revision -m 'first migration' --autogenerate
```

To apply the migrations to your database, run:

 ```bash
alembic upgrade head
```

To connect the pgadmin4 you can use next variable:
```
USER='user'
PASSWORD='password'
DB_NAME='database'
PORT='5431'
HOST='localhost'

```