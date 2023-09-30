## Advanced Configuration Options

`config.json` contains all the information about the images to be downloaded.

Where supported, date/time substitutions must be in the format given by the [strftime documentation](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior).

Each image can have the following settings:

 - `time_zone`: Required. A string representing the time zone of the region this weather briefing is for.
 - `working_dir`: Required. The directory in which the downloaded images should be saved, written as an array of directory names. It is relative to the home directory and supports date/time substitutions. It will be created if it doesn't exist.
 - `items`: An array containing information about the images to be downloaded. For each `item`, the following options are supported:
   - `name`: Required. Used in the file name and slide title.
   - `url`: Required. Supports date/time substitutions.
   - `times`: Optional. An array of local times to be substituted into the URL. More than one time means more than one image will be downloaded.
   - `utc`: Optional. Set this to a truthy value (like `true`) to tell the downloader that the times must be converted to UTC before being substituted into the URL.
   - `image_includes_caption`: Optional. Set this to a truthy value if the title box should be omitted from the slide.
   - `show_by_default`: Optional. Slides are hidden by default (because a briefing should be brief). Set this to `true` to show all slides for this item, or provide an array of the times for which slides should be shown.