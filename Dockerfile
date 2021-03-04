FROM ghcr.io/uccser/django:2.2.18

RUN apt-get update \
    && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin

ENV DJANGO_PRODUCTION=True
LABEL maintainer="csse-education-research@canterbury.ac.nz"
EXPOSE 8080

# Copy and install dependencies inside virtual environment
COPY requirements /requirements
RUN /docker_venv/bin/pip3 install -r /requirements/production.txt

RUN mkdir /dthm4kaiako
WORKDIR /dthm4kaiako

# Copy website and set entrypoint
COPY ./dthm4kaiako/ /dthm4kaiako/
CMD /dthm4kaiako/docker-production-entrypoint.sh
