## Development environment setup

### Prerequisites
 - Python 3.12 or higher
 - Git
 - [uv](https://github.com/astral-sh/uv) (see [installation instructions](https://docs.astral.sh/uv/getting-started/installation/))

### Clone the repository
```
git clone https://github.com/demccormack/weatherdl.git
cd weatherdl
```

### Set up the development environment
uv automatically creates a virtual environment and installs all dependencies from the lock file:
```
uv sync --all-extras
```

### Run the project
```
uv run python src/main.py
```

## Testing

The test suite runs in CI on every push. You can also run it locally with
```
uv run pytest
```

## Formatting

The code is checked in CI by `pylint` linter and `black` formatter on every
push. You can also run linting locally with
```
uv run pylint $(git ls-files '*.py')
```
and formatting with
```
uv run black .
```

If you're using VS Code, you can make all this happen automatically by installing the following extensions
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)

VS Code will automatically detect the `.venv` virtual environment created by uv. Set the following VS Code settings for automatic formatting:
```
{
  "files.autoSave": "onFocusChange",
  "[python]": {
      "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "editor.formatOnSave": true
}
```

## Building

To create distributable binaries, use:
```
uv run PyInstaller \
  -n weatherdl \
  --onefile \
  --add-data "./.venv/lib/*/site-packages/pptx/templates:pptx/templates" \
  src/main.py \
  && cp -f ./config.json ./dist/
```

## Adding dependencies

- **Production dependencies**: Add to the `dependencies` array in `pyproject.toml`
- **Development dependencies**: Add to `[project.optional-dependencies.dev]` in `pyproject.toml` 
- **Build dependencies**: Add to `[project.optional-dependencies.build]` in `pyproject.toml`

After editing `pyproject.toml`, run:
```
uv lock
```
to update the lock file with resolved versions.
