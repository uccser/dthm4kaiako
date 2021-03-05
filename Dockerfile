FROM ghcr.io/uccser/django:2.2.18

RUN apt-get update \
    && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin

ENV DJANGO_PRODUCTION=True
ENV DJANGO_SETTINGS_MODULE="config.settings.production"
LABEL maintainer="csse-education-research@canterbury.ac.nz"
EXPOSE 8080

# Copy and install dependencies inside virtual environment
COPY requirements /requirements
RUN /docker_venv/bin/pip3 install -r /requirements/production.txt

# Copy website and run entrypoint script
RUN mkdir /dthm4kaiako/
COPY ./dthm4kaiako/ /dthm4kaiako/
WORKDIR /dthm4kaiako/
CMD /dthm4kaiako/docker-production-entrypoint.sh
