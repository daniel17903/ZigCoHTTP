FROM python:buster

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Bundle app source
COPY . /usr/src/app

# Environment variables
ENV PORT 8484
ENV DEVICE "/dev/ttyS0"
ENV DATABASE_FILE "devices.db"

# Port to listener
EXPOSE 8484

# Main command
CMD [ "python", "main.py" ]