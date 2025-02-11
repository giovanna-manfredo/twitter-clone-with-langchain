FROM python:3.13

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -xzvf dockerize-linux-amd64-v0.6.1.tar.gz -C /usr/local/bin \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz

WORKDIR /app   

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root

COPY . /app/

EXPOSE 8000

CMD ["poetry", "run", "python", "./backend/manage.py", "runserver", "0.0.0.0:8000"]
