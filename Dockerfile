FROM uccser/django:1.11.11

# Add metadata to Docker image
LABEL maintainer="csse-education-research@canterbury.ac.nz"

# Set terminal to be noninteractive
ARG DEBIAN_FRONTEND=noninteractive
ENV DJANGO_PRODUCTION=True

EXPOSE 8080
RUN mkdir /cs4teachers
WORKDIR /cs4teachers

# Copy and install Python dependencies
COPY requirements /requirements
RUN /docker_venv/bin/pip3 install -r /requirements/production.txt

ADD ./cs4teachers /cs4teachers/

CMD /cs4teachers/docker-production-entrypoint.sh
