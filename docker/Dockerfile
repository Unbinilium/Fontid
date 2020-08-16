FROM python:3.8-slim

EXPOSE 8080

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt --use-feature=2020-resolver

WORKDIR /app
ADD app /app
COPY src/app.py /app.py

VOLUME [ "/data" ]

# Switching to a non-root user
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden
CMD ["python", "/app.py", "/data/config.json"]
