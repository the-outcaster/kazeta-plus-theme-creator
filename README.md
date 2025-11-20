# Kazeta+ Theme Creator

![Screenshot of the application](https://i.imgur.com/Uhk0u0d.png)

GUI application for creating and editing themes for [Kazeta+](https://github.com/the-outcaster/kazeta-plus). See the [Kazeta+ Wiki page](https://github.com/the-outcaster/kazeta-plus/wiki/Making-Your-Own-Themes) for more info.

## Downloads
You'll need [FFmpeg](https://ffmpeg.org/download.html#build-linux) installed before running -- this is for for audio file conversion.

Pre-built AppImages are available on the [Releases](https://github.com/the-outcaster/kazeta-plus-theme-creator/releases) page.

## Building from Source

Prerequisites:
* `python3.12`
* `ffmpeg`

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/the-outcaster/kazeta-plus-theme-creator.git
    cd kazeta-plus-theme-creator
    ```

2.  **Create a Python 3.12 virtual environment:**
    ```bash
    python3.12 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the Python dependencies:**
    Create a `requirements.txt` file with the following content:
    ```
    toml
    Pillow
    pydub
    ```
    Then, install the requirements:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```

### Building the AppImage

A helper script is included in the repo to build the AppImage.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run the build script:**
    ```bash
    chmod +x build-appimage.sh
    ./build-appimage.sh
    ```
    The script will automatically download `appimagetool`, bundle the application, and place the `.AppImage` in `~/Applications/`.

## Acknowledgments

* Thanks to **Alkazar** for the original [Kazeta](https://github.com/kazetaos/kazeta) project.
