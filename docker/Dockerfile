FROM python:3.8-slim

# Container port
EXPOSE 8080

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Add src
WORKDIR /src
ADD src /src

# Install pip requirements
RUN python -m pip install -r /src/requirements.txt --use-feature=2020-resolver

# Add app.py
ADD app.py .

# Create /tmp
RUN mkdir /tmp

# Create volume
VOLUME [ "/data" ]

# Switching to a non-root user
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden
CMD ["python", "/app.py", "/data/config.json"]
