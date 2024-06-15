1. Build the Docker Image

Build the Docker image using the following command:

docker build -t receipt-processor .

2. Run the Docker Container

Run the Docker container with the following command:

docker run -p 5000:5000 receipt-processor
The service will be available at http://localhost:5000.

