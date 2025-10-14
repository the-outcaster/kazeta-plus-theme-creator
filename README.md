# Kazeta+ Theme Creator

![Screenshot of the application](https://i.imgur.com/Uhk0u0d.png)

A simple, user-friendly GUI application for creating and editing themes for the [Kazeta+](https://github.com/the-outcaster/kazeta-plus) game launcher. This tool streamlines the entire theme creation process, from bundling assets to generating the final `theme.toml` file.

---

## Features ✨

* **Create from Scratch**: Easily create new themes with a straightforward graphical interface.
* **Load & Edit**: Open an existing `theme.toml` file to load and modify a theme you've already created.
* **Full Theming Control**: Access all `theme.toml` options, including colors, menu positions, and scroll speeds, through simple dropdowns and text fields.
* **Automatic Asset Conversion**:
    * Converts BGM tracks (e.g., MP3, WAV) to the required `.ogg` format.
    * Converts logo and background images (e.g., JPG) to the required `.png` format.
    * Converts SFX sound files from `.ogg` to the required `.wav` format.
* **Smart Folder Export**: Automatically creates a clean, ready-to-use theme folder with all assets correctly named and organized.
* **Overwrite Protection**: Asks for confirmation before overwriting an existing theme folder.

---

## Getting Started (for Users) 🚀

The easiest way to run the application is by using the pre-built AppImage.

### Runtime Dependency

Before you start, you **must** have **FFmpeg** installed on your system. The application uses it for audio file conversion.

* **On Fedora/CentOS:**
    ```bash
    sudo dnf install ffmpeg
    ```
* **On Debian/Ubuntu:**
    ```bash
    sudo apt-get install ffmpeg
    ```

### Installation

1.  Go to the **[Releases](https://github.com/the-outcaster/kazeta-plus-theme-creator/releases)** page of this project.
2.  Download the latest `KazetaThemeCreator-vX.X-x86_64.AppImage` file.
3.  Make the file executable:
    ```bash
    chmod +x KazetaThemeCreator-*.AppImage
    ```
4.  Run it!
    ```bash
    ./KazetaThemeCreator-*.AppImage
    ```

---

## Building from Source (for Developers) 🛠️

If you prefer to run or build the application from its source code, follow these steps.

### Prerequisites

* **Python 3.12**: This version is required because the `pydub` library depends on the `audioop` module, which was removed in Python 3.13.
* **FFmpeg**: See the installation instructions above.

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

The repository includes a helper script to build the AppImage.

1.  **Create an icon:** Make sure you have an application icon named `kazeta_icon.png` in the project's root directory. A 256x256 pixel image is recommended.

2.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

3.  **Run the build script:**
    ```bash
    chmod +x build-appimage.sh
    ./build-appimage.sh
    ```
    The script will automatically download `appimagetool`, bundle the application, and place the final `.AppImage` file in a new `release/` directory.

## Acknowledgments

* Thanks to **Alkazar** for the original [Kazeta](https://github.com/kazetaos/kazeta) project.
