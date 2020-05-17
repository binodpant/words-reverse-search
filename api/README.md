To run this we need an .env file (not checked into git by default) here

contents of the file must have the following (or updated as needed for prod)

```json
FLASK_APP=api.py
FLASK_ENV=development
ES_HOST=words-reverse-match-5971522899.us-east-1.bonsaisearch.net
ES_PORT=443
ES_AUTH_USER=********
ES_AUTH_PWD=******

```