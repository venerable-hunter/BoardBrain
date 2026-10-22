# Start and Stop Scripts

This directory contains scripts to start and stop the Docker container for the Project Management MVP.

## Scripts

### Mac/Linux
- `start.sh` - Builds and starts the Docker container
- `stop.sh` - Stops and removes the Docker container

### Windows
- `start.bat` - Builds and starts the Docker container
- `stop.bat` - Stops and removes the Docker container

## Usage

### Mac/Linux
```bash
# Start
./scripts/start.sh

# Stop
./scripts/stop.sh
```

### Windows
```cmd
# Start
scripts\start.bat

# Stop
scripts\stop.bat
```

## What the scripts do

### start.sh / start.bat
1. Builds the Docker image with tag `pm-mvp`
2. Runs the container in detached mode
3. Maps port 8000 on host to port 8000 in container
4. Names the container `pm-mvp-container`

### stop.sh / stop.bat
1. Stops the running container
2. Removes the container

## Accessing the app
After starting, access the application at http://localhost:8000