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

## Prepare your briefing
The script has created a new directory full of today's weather images as well as a PPTX file already populated with them. Open this file and hide/unhide the slides relevant to today's briefing. Add your own title, summary and goodbye slides and you are good to go!

### Missing images
You may need to re-run the script in order to download an image that wasn't available before. When you do this, a new PPTX file will be created. The original file is safe and your partially-prepared briefing won't be overwritten. However you will need to manually insert the missing image.

## Advanced

The following is a summary of the supported configuration options in `config.json`. Where supported, date/time substitutions must be in the format given by the [strftime documentation](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior).

 - `time_zone`: Required. A string representing the time zone of the region this weather briefing is for.
 - `working_dir`: Required. The directory in which the downloaded images should be saved. It will be created if it doesn't exist. It can be a full or relative path and supports date/time substitutions.
 - `items`: An array containing information about the images to be downloaded. For each `item`, the following options are supported:
   - `name`: Required. Used in the file name and slide title.
   - `url`: Required. Supports date/time substitutions.
   - `times`: Optional. An array of local times to be substituted into the URL. More than one time means more than one image will be downloaded.
   - `utc`: Optional. Set this to a truthy value (like `true`) to tell the downloader that the times must be converted to UTC before being substituted into the URL.
   - `image_includes_caption`: Optional. Set this to a truthy value if the title box should be omitted from the slide.
   - `show_by_default`: Optional. Slides are hidden by default (because a briefing should be brief). Set this to `true` to show all slides for this item, or provide an array of the times for which slides should be shown.

## Troubleshooting
If you get the following error,
```
ImportError: failed to find libmagic. Check your installation
```
ensure `libmagic` is installed on your system (at the OS level) and then try again.