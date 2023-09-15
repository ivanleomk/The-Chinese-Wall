# Introduction

Welcome to our repository for the Chinese Wall Challenge for the UBS Coding
Challenge. During this challenge, users need to trick a LLM into revealing a
password that it's not supposed to.

This project is built using python, FastAPI and Postgresql. We utilise a few
other services such as Upstash and Neon to help us with the challenge.

## Installation Instructions

You'll need to install all the local packages as required.

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

We have configured logging of user attempts into a persistent Postgresql
database with some basic rate limiting. To enable those, you'll need to setup a
Postgresql database and set the environment variables accordingly. You can find
our database schema in [schema.sql](./schema.sql)

We have a deployed version currently at
https://cis2023-thechinesewall-6f0e2f1f2dfa.herokuapp.com/
