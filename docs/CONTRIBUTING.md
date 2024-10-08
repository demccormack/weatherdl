## Development environment setup

### Prerequisites
 - Python 3.12
 - Git

### Clone the repository
```
git clone https://github.com/demccormack/weatherdl.git
cd weatherdl
```

### Set up the virtual environment
On MacOS/Linux
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements-prod.txt -r requirements-dev.txt
```
or on Windows
```
python -m venv venv
.\venv\Scripts\activate.ps1
python -m pip install -r requirements-prod.txt -r requirements-dev.txt
```

### Run the project
```
python3 src/main.py
```

## Testing

The test suite runs in CI on every push. You can also run it locally with
```
pytest
```

## Formatting

The code is checked in CI by `pylint` linter and `black` formatter on every
push. You can also run linting locally with
```
pylint $(git ls-files '*.py')
```
and formatting with
```
black .
```

If you're using VS Code, you can make all this happen automatically by installing the following extensions
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)

and setting the following VS Code settings
```
{
  "files.autoSave": "onFocusChange",
  "[python]": {
      "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "editor.formatOnSave": true
}
```
