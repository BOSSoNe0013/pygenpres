# PyGenPres
PyGenPres is a Python application for generating presentations programmatically.

## Features
*   Create slides with text, images, and videos.
*   Customize slide layouts and themes.
*   Add transitions and animations.
*   Export presentations to various formats (e.g., HTML, PDF).

## Installation
Clone the repository then cd into the project directory, create a python virtual environment and install requirements.
``` bash
git clone {git_url}
cd {project_name}
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
### Dev mode
Run the following command to start the development server:
```bash
fastapi dev app
```
Then open http://localhost:8000 in your browser.

### Docker
Create a directory to store your presentations and update the dockerfile :
``` yaml
    - {YOUR_STORAGE_DIRECTORY}:/root/.config/pygenpres
```

Then build and run the app with this command :
``` bash
docker-compose up --build
```

## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues.

## License
This project is licensed under the GPLv3 License.
