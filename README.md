# WakeOnLanService

![Test Status](https://github.com/FroeFam/WakeOnLanService/actions/workflows/main.yml/badge.svg?branch=main)

## Development Instructions

### Initial Set Up

1. Clone this repo

1. Create a virtual environment

   Python virtual environments allow you to install Python packages in a location isolated from the rest of your system instead of installing them system-wide.

   You can learn more about virtual environments on the [Python.land website](https://python.land/virtual-environments/virtualenv)

1. Activate the virtual environment

1. Install Poetry

    Package management is handled via Poetry.
    If you don't have Poetry installed, you can install it by following the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).

1. Install Dependencies

   `poetry install`

1. Set Up Environment Variables

   Create a `.env` file in the root directory of the project and add the necessary environment variabless:

   ```env
   FLASK_APP=src.app
   FLASK_ENV=development
   FLASK_DEBUG=1
   MAC_ADDRESS=your_mac_address_here
   URL=your_url_here
   REDIRECT_ON_AVAILABLE=true
   ```

   `URL` is polled until it answers HTTP 200. `REDIRECT_ON_AVAILABLE` (default `true`) decides what happens next: `true` sends the browser to `URL`; `false` (also `0`, `no`, `off`) shows a "Success - The computer is on." screen instead and does not return `URL` to the browser, so `URL` can be an internal address.

1. Run the Flask Application

   With the virtual environment activated and environment variables set, you can now run your Flask application:

   ```sh
   flask run --host=0.0.0.0 --port=5000
   ```

   Access the application by opening your web browser and navigating to <http://127.0.0.1:5000/>.

### Optional VSCode Set Up

If you want to use VSCode for development, create a `.vscode\launch.json`

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/src/wakeonlanservice/app.py",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src",
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "true",
                "URL": you_url_here,
                "MAC_ADDRESS": your_mac_address_here
            },
            "args": [],
            "jinja": true
        }
    ]
}
```

## Build and Test Instructions

### Building for docker

Run `build.ps1` to build docker container.

Run `build.ps1 -Run` to build and run the container.

### Testing

To run tests, simply run command `poetry run pytest`. This will run all tests.

If you only want to run unit tests, run: `poetry run pytest tests/unit`

## Release Process

To release a new version of the application:

1. Make sure all your changes have been merged to the `main` branch
2. Create a new tag with the format `release/x.y.z` (e.g., `release/1.0.0`) where x.y.z follows semantic versioning
3. Push the tag to GitHub:
   ```sh
   git tag release/1.0.0
   git push origin release/1.0.0
   ```
4. The GitHub Actions workflow will automatically:
   - Run linting checks
   - Run unit tests for supported python versions
   - Run integration tests
   - Build the Docker image
   - Push the Docker image to Docker Hub with tags matching the version and 'latest'

Note: You need to have the Docker Hub credentials configured as secrets in your GitHub repository (`DOCKER_USERNAME` and `DOCKER_PASSWORD`).

## Dockerhub

Docker container can be found at <https://hub.docker.com/r/drache42/wakeonlanservice>