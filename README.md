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
#### 4.1 Build the Docker image

Run the command to build the Docker image(my-fastapi-poetry-app change it to your image name):

```bash
docker build -t my-fastapi-poetry-app .

```

#### 4.2 Create and Run Docker container

my-fastapi-poetry-container - name of your container;
my-fastapi-poetry-app - name of your image;

```bash
docker run --env-file .env.docker -d --name my-fastapi-poetry-container -p 8000:8000 my-fastapi-poetry-app
```
