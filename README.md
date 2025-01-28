# YouTube Video & Audio Downloader

This Python script allows you to download YouTube videos and audio in various formats (MP3, WAV, MP4, and WEBM) using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Features

- Download YouTube videos and audio in multiple formats (MP3, WAV, MP4, WEBM).
- Choose video resolution and audio bitrate for optimal quality.
- Supports both single and batch download modes.
- Interactive console with rich progress and error logging.
- Customizable storage path for saving downloads.

## Requirements

- **Python 3.x**
- **yt-dlp** - Install via `pip install yt-dlp`
- **rich** - Install via `pip install rich`

## How to Use

1. Clone or download this repository to your local machine.
2. Install the required dependencies:
    ```bash
    pip install yt-dlp rich
    ```
3. Run the script:
    ```bash
    python yt.py
    ```
4. Choose between single or batch download mode.
5. Provide the YouTube URL(s), select your desired format and quality, and the download will begin.

## Download Options

During download, you can choose from the following formats:

- **MP3** (Audio)
- **WAV** (Audio)
- **MP4** (Video)
- **WEBM** (Video)

## Customization

You can specify a custom path for storing the downloaded files. If not provided, the default path is set to `/sdcard/Download`.

## Logging

The script logs all activities and errors to `download_log.txt` for future reference. Check this file if you encounter any issues.

## Troubleshooting

- If you encounter a "Permission Denied" error, make sure the script has proper access to the specified storage path.
- Ensure you have an active internet connection for downloading content.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make changes, and submit pull requests.

## Api
Soon
