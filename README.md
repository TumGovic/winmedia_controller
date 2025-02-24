# winmedia_controller

A simple Python library for controlling and monitoring media playback on Windows using hotkeys and the Windows Media Control API.

WARN: Please install package winrt manualy, my script is 100% work!

## Overview

`winmedia_controller` allows you to control media playback (play/pause, next track, previous track) and retrieve information about the currently playing media (e.g., title, artist, album, playback status, progress) on Windows. It uses hotkeys for easy control and supports asynchronous operations for efficient media monitoring.

## Features
- Toggle playback (play/pause) with a hotkey.
- Skip to the next or previous track using hotkeys.
- Monitor real-time media information (title, artist, album, playback status, progress, etc.).
- Asynchronous design for non-blocking operations.
- Easy integration with any Windows media player supporting the Media Control API.

## Requirements
- **Operating System**: Windows (the library uses Windows-specific APIs).
- **Python**: 3.7 or higher.
- **Dependencies**:
  - `winrt-python` (for Windows Runtime support)
  - `keyboard` (for hotkey functionality)

## Installation

1. Clone or download this repository to your local machine.
2. Navigate to the root directory of the project.
3. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not present, install the dependencies manually:

   ```bash
   pip install winrt-python keyboard
   ```

4. (Optional) Install the library locally for development:

   ```bash
   pip install -e .
   ```

## Usage

Here’s a simple example of how to use `winmedia_controller` to control media and monitor playback:

```python
import asyncio
from winmedia_controller.media_controller import MediaController

async def print_media_info():
    controller = MediaController()
    while True:
        info = await controller.get_media_info()
        if info:
            print(f"Media Info: {info}")
        await asyncio.sleep(1)  # Check every second

async def main():
    controller = MediaController()
    await print_media_info()

if __name__ == "__main__":
    asyncio.run(main())
```

### Hotkeys
By default, the library uses the following hotkey combinations:
- `play/pause media`: Toggles playback (play or pause).
- `next track`: Skips to the next track.
- `previous track`: Skips to the previous track.

You can modify these hotkeys by editing the `_setup_hotkeys` method in `media_controller.py`.

### Monitoring Media
The `monitor` method allows you to continuously monitor media playback and call a callback function with the current media information:

```python
async def on_media_update(info):
    print(f"Current song: {info['title']} by {info['artist']} - {info['status']}")

controller = MediaController()
await controller.monitor(callback=on_media_update, interval=1)  # Check every second
```

## Building the Library
To build and distribute `winmedia_controller` as a Python package:

1. Ensure `setup.py` and `pyproject.toml` are properly configured with project metadata and dependencies.
2. Run the following command to build the package:

   ```bash
   python setup.py sdist bdist_wheel
   ```

3. Install the built package locally:

   ```bash
   pip install dist/winmedia_controller-0.1.0-py3-none-any.whl
   ```

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss what you’d like to change.

## License
This project is licensed under the [MIT License](LICENSE) - see the `LICENSE` file for details.

## Support
If you encounter any issues or have questions, please open an issue on this repository or contact [your contact information here].