# syntax=docker/dockerfile:1
FROM python:3.8
# Install python dependencies
WORKDIR /code
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
COPY poetry.lock pyproject.toml /code
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-dev
# Install hardware interactions
RUN pip3 install RPi.GPIO
# Copy and run application
COPY . /code
EXPOSE 80
CMD ["bokeh", "serve" "app.py", "--address=0.0.0.0", "--port=80", "--allow-websocket-origin=*"]
