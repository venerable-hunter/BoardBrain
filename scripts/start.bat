@echo off

REM Build the Docker image
docker build -t pm-mvp .

REM Run the Docker container
docker run -d -p 8000:8000 --name pm-mvp-container pm-mvp

echo Container started. Access the app at http://localhost:8000
