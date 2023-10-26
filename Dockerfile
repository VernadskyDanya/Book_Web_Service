ARG FROM_IMAGE=python:3.10-slim-bullseye

FROM $FROM_IMAGE

ARG UID=1000
ARG GID=1000

ENV PYTHONUNBUFFERED=1

ENV TZ=Europe/Latvia

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


# Install app deps
COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false && \
    poetry install --only main && \
    rm poetry.lock pyproject.toml

# Copy app
COPY src /opt/app
RUN chmod -R a=r-wx,u=rw,a+X /opt/app

# Add app user, grant app dir permissions
RUN addgroup app --gid $GID --system  && \
    adduser app --uid $UID --system --ingroup app && \
    chown -R app:app /opt/app

# Add entrypoint
COPY docker-entrypoint.sh /
RUN chmod 755 /docker-entrypoint.sh

# Run app
USER app:app
WORKDIR /opt/app
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["run"]
#ENTRYPOINT ["/bin/bash"]