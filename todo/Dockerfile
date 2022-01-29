FROM python:3.10-alpine
WORKDIR /app

# Console output looks good and no buffering
ENV PYTHONUNBUFFERED 1
# Do not create *.pyc files
ENV PYTHONDONTWRITEBYTECODE 1


COPY requirements.txt .

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all project files from current dir to WORKDIR
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]