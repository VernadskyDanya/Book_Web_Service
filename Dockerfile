ARG FROM_IMAGE=python:3.10-slim-bullseye

# Stage 1: Build stage for dependencies and configurations
FROM $FROM_IMAGE AS dependencies_stage

ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

# Update and install system deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        libpq-dev \
        python3-dev \
        gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install poetry==1.6.1

# Install app dependencies
COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false && \
    poetry install --only main && \
    rm poetry.lock pyproject.toml

# Stage 2: Build stage for frequently changing code
FROM dependencies_stage AS code_stage

ARG UID=1000
ARG GID=1000

# Copy app
COPY src /opt/app
RUN chmod -R a=r-wx,u=rw,a+X /opt/app

# Add app user, grant app directory permissions
RUN addgroup app --gid $GID --system  && \
    adduser app --uid $UID --system --ingroup app && \
    chown -R app:app /opt/app

# Add entrypoint
COPY docker-entrypoint.sh /
RUN chmod 755 /docker-entrypoint.sh

# Stage 3: Final stage for creating the production image
FROM dependencies_stage AS production_stage

# Copy dependencies and configurations
COPY --from=dependencies_stage / /

# Copy code from the code stage
COPY --from=code_stage /opt/app /opt/app

# Set the working directory
WORKDIR /opt/app

# Change user to the app user
USER app:app

# Entrypoint or command to start the application
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["run"]