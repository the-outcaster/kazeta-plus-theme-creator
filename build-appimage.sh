#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
APP_NAME="Kazeta-Plus-Theme-Creator"
VERSION="1.2"
MAIN_SCRIPT="main.py"
ICON_NAME="kazeta_icon.png"

# --- Build paths are now in /tmp ---
BUILD_PATH="/tmp/${APP_NAME}_build"
DIST_PATH="/tmp/${APP_NAME}_dist"
APPDIR="/tmp/${APP_NAME}.AppDir"

# --- Final output directory and tool path ---
OUTPUT_DIR="${HOME}/Applications"
APPIMAGE_TOOL_PATH="${OUTPUT_DIR}/appimagetool-x86_64.AppImage"

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
cp "$ICON_NAME" "$APPDIR/"

echo "Creating .desktop file..."
cat <<EOF > "$APPDIR/$APP_NAME.desktop"
[Desktop Entry]
Name=$APP_NAME
Exec=$APP_NAME
Icon=$(basename "$ICON_NAME" .png)
Type=Application
Categories=Utility;Development;
EOF

echo "Creating AppRun script..."
cat <<EOF > "$APPDIR/AppRun"
#!/bin/bash
HERE="\$(dirname "\$(readlink -f "\${0}")")"
exec "\$HERE/$APP_NAME" "\$@"
EOF
chmod +x "$APPDIR/AppRun"

echo "--- 4. Checking for appimagetool in $OUTPUT_DIR ---"
# Ensure the ~/Applications directory exists
mkdir -p "$OUTPUT_DIR"
if [ ! -f "$APPIMAGE_TOOL_PATH" ]; then
    echo "Downloading appimagetool to $APPIMAGE_TOOL_PATH..."
    wget -O "$APPIMAGE_TOOL_PATH" "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x "$APPIMAGE_TOOL_PATH"
else
    echo "appimagetool already exists."
fi

echo "--- 5. Building the AppImage ---"
# Build the AppImage and place it in the local directory
ARCH=x86_64 VERSION="$VERSION" "$APPIMAGE_TOOL_PATH" "$APPDIR"

echo "--- 6. Moving AppImage and cleaning up ---"
# Move the final AppImage to the output directory
mv "${APP_NAME}-${VERSION}-x86_64.AppImage" "$OUTPUT_DIR/"

# Clean up only the .spec file
rm -f "${APP_NAME}.spec"

echo ""
echo "✅ Success!"
echo "AppImage created in: $OUTPUT_DIR"
echo "Build files are located in /tmp (build_path, dist_path, AppDir)."
