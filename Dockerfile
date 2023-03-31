# Base image
FROM python:3.10.1

# Set the environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry
RUN pip install poetry

# Set up the working directory
RUN mkdir /b2b_shop
WORKDIR /b2b_shop
COPY poetry.lock /b2b_shop/
COPY pyproject.toml /b2b_shop/
COPY . /b2b_shop/

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Run the application
CMD ["poetry", "run", "python", "manage.py", "runserver"]
