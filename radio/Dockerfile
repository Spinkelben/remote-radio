#Use debian base image, it comes with python
FROM debian:jessie

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install PyGObject bindings
RUN apt-get update && apt-get install -y \
#    gir1.2-ges-1.0 \
    gir1.2-gstreamer-1.0 \
    gir1.2-gst-plugins-base-1.0 \
    gir1.2-gtk-3.0 \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
#    gstreamer1.0-plugins-ugly \
    gstreamer1.0-alsa \
    gstreamer1.0-pulseaudio \
    gstreamer1.0-libav \
#    libges-1.0 \
    pulseaudio  \
    python3-gst-1.0 \
    python3-gi

RUN usermod -a -G audio root


# Install any needed packages specified in requirements.txt
#RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD ["python3", "test.py"]
