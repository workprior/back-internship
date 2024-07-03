# My FastAPI Project

Here are the instructions on how to run this project locally.

## Requirements

- Python 3.7 or later
- pip (Python package installer)
- virtualenv (recommended for environment isolation)

## Installation

### 1. Clone the repositoryasd

Clone this repository to your local environment:

```bash
git clone https://github.com/workprior/back-internship.git
cd back-internship
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
### 4. Set up environment variables

```bash
cp .env.sample .env
```
## Running the application

Start the development server:
```bash
uvicorn app.main:app --reload
```
The web application will be available at 'http://127.0.0.1:8000'.

## Testing

To run tests, use pytest:
```bash
pytest
```