FROM python:3.10
LABEL maintainer="Trung Dan Phan @trung_dan_phan"

WORKDIR /app

# Install Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock to the container
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry (without creating a virtual environment)
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Copy the entire app directory
COPY . /app

# Expose the port that Streamlit will run on
EXPOSE 8501

# Health check to verify if the app is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Set the entry point for the container to run the Streamlit app
ENTRYPOINT ["streamlit", "run"]

# Set the default command to start the Streamlit app
CMD ["src/Home.py"]
