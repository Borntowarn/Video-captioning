# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# set the environment variable for the port (default is 8080)
ENV PORT 8080
ENV NN_API_URL "http://localhost:8081"

# expose the port
EXPOSE $PORT

ENTRYPOINT ["python"]

CMD [ "main.py" ]