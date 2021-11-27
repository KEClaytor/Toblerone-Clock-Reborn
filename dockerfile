# syntax=docker/dockerfile:1
FROM python:3.8
# Install python dependencies
WORKDIR /code
# No sense building these packages, they take quite a long time on the zero
RUN sudo apt install python3-numpy python3-pandas
# Other python dependnencies
RUN pip3 install bokeh
# Hardware interaction
RUN pip3 install RPi.GPIO adafruit-circuitypython-neopixel
# Copy and run application
COPY . /code
EXPOSE 80
CMD ["bokeh", "serve" "app.py", "--address=0.0.0.0", "--port=80", "--allow-websocket-origin=*"]
