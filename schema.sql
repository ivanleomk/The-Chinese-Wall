CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP,
  level TEXT,
  prompt TEXT,
  response TEXT
);
