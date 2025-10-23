#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
APP_NAME="KazetaThemeCreator"
VERSION="1.1"
MAIN_SCRIPT="main.py"
ICON_NAME="kazeta_icon.png" # You need to create this icon file

# --- UPDATE: Build paths are now in /tmp ---
BUILD_PATH="/tmp/${APP_NAME}_build"
DIST_PATH="/tmp/${APP_NAME}_dist"
APPDIR="/tmp/${APP_NAME}.AppDir"

# --- UPDATE: Final output directory is ~/Applications ---
OUTPUT_DIR="${HOME}/Applications"

echo "--- 1. Cleaning up old temporary builds from /tmp ---"
rm -rf "$BUILD_PATH" "$DIST_PATH" "$APPDIR"
mkdir -p "$BUILD_PATH" "$DIST_PATH"

echo "--- 2. Building standalone Python binary with PyInstaller (in /tmp) ---"
pyinstaller --noconfirm --onedir --windowed \
            --name "$APP_NAME" \
            --icon="$ICON_NAME" \
            --workpath "$BUILD_PATH" \
            --distpath "$DIST_PATH" \
            "$MAIN_SCRIPT"

echo "--- 3. Preparing the AppDir structure (in /tmp) ---"
mkdir -p "$APPDIR"
mv "$DIST_PATH"/"$APP_NAME"/* "$APPDIR/"

# Copy the application icon into the AppDir
cp "$ICON_NAME" "$APPDIR/"

# Create the .desktop file for menu integration
echo "Creating .desktop file..."
cat <<EOF > "$APPDIR/$APP_NAME.desktop"
[Desktop Entry]
Name=$APP_NAME
Exec=$APP_NAME
Icon=$(basename "$ICON_NAME" .png)
Type=Application
Categories=Utility;Development;
EOF

# Create the AppRun entry script
echo "Creating AppRun script..."
cat <<EOF > "$APPDIR/AppRun"
#!/bin/bash
HERE="\$(dirname "\$(readlink -f "\${0}")")"
exec "\$HERE/$APP_NAME" "\$@"
EOF
chmod +x "$APPDIR/AppRun"

echo "--- 4. Downloading appimagetool ---"
if [ ! -f appimagetool-x86_64.AppImage ]; then
    wget "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x appimagetool-x86_64.AppImage
fi

echo "--- 5. Building the AppImage ---"
# This creates the AppImage in the local directory
ARCH=x86_64 VERSION="$VERSION" ./appimagetool-x86_64.AppImage "$APPDIR"

echo "--- 6. Moving AppImage to $OUTPUT_DIR ---"
# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Move the final AppImage
mv "${APP_NAME}-${VERSION}-x86_64.AppImage" "$OUTPUT_DIR/"

# Clean up the downloaded tool
rm -f appimagetool-x86_64.AppImage

echo ""
echo "✅ Success!"
echo "AppImage created in: $OUTPUT_DIR"
echo "Build files are located in /tmp (build_path, dist_path, AppDir)."
