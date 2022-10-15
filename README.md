# Weather Downloader
This script downloads all the images required for a weather briefing in Omarama, New Zealand. They can then be imported into PowerPoint.

## Quick Start

### Clone the repository
```
git clone https://github.com/demccormack/weatherdl.git
cd weatherdl
```

### Set up the virtual environment
(commands are for MacOS/Linux)
```
python3 -m venv weatherdl_venv
source weatherdl_venv/bin/activate
pip install -r requirements.txt
```
   
## Run it!
```
python3 src/weatherdl.py
```

### Use the results
The script has created a new directory full of today's weather images. Open PowerPoint or LibreOffice and use the import feature to create a new presentation from the image collection. Hide the ones you don't need and you are good to go!

## Troubleshooting
If you get the following error,
```
ImportError: failed to find libmagic. Check your installation
```
ensure `libmagic` is installed on your system (at the OS level) and then try again.