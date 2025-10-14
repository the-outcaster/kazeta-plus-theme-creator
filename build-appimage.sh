#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
APP_NAME="KazetaThemeCreator"
VERSION="1.0"
MAIN_SCRIPT="main.py"
ICON_NAME="logo.png"
APPDIR="$APP_NAME.AppDir"
RELEASE_DIR="release"

echo "--- 1. Cleaning up old builds ---"
rm -rf build dist "$APPDIR" "$RELEASE_DIR" "$APP_NAME"*.AppImage

echo "--- 2. Building standalone Python binary with PyInstaller ---"
pyinstaller --noconfirm --onedir --windowed \
            --name "$APP_NAME" \
            --icon="$ICON_NAME" \
            "$MAIN_SCRIPT"

echo "--- 3. Preparing the AppDir structure ---"
mkdir -p "$APPDIR"
mv dist/"$APP_NAME"/* "$APPDIR/"
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

echo "--- 4. Downloading appimagetool ---"
if [ ! -f appimagetool-x86_64.AppImage ]; then
    wget "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x appimagetool-x86_64.AppImage
fi

echo "--- 5. Building the AppImage ---"
ARCH=x86_64 VERSION="$VERSION" ./appimagetool-x86_64.AppImage "$APPDIR"

echo "--- 6. Organizing and cleaning up files ---"
# Create the release directory
mkdir -p "$RELEASE_DIR"

# Move the final AppImage into the release directory
mv "${APP_NAME}-${VERSION}-x86_64.AppImage" "$RELEASE_DIR/"

# Clean up all intermediate files and folders
rm -rf build dist "$APPDIR" appimagetool-x86_64.AppImage *.spec

echo ""
echo "✅ Success!"
echo "AppImage has been moved to the '$RELEASE_DIR' folder."
