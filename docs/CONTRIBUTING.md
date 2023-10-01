## Development environment setup

### Prerequisites
 - Python 3.11
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

### Run the script
```
python3 src/main.py
```
