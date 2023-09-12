# the-chinese-wall

## Getting Started

```bash
# Create a new virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Start the application
python3 main.py
```

## Development

https://cis2023-thechinesewall-6f0e2f1f2dfa.herokuapp.com/

## Documentation

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Create the db table for logs

```
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    level VARCHAR(255) NOT NULL,
    prompt VARCHAR(255) NOT NULL,
    response VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);
```
