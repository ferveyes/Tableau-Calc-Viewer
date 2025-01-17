# Tableau-Calc-Viewer
This tool is an aid for efficient analysis of calculated fields in Tableau. You can launch any number of calculated field windows simultaneously. It is very easy to use!
1. Download this repository as a ZIP file and unzip it to a location of your choice.
2. There is an exe file in the dist folder. Place the workbook (twb or twbx file) you wish to analyze in this location.
3. Open the workbook you wish to analyze.
4. Double click on the exe file to start it.
5. Press the Scan button and confirm that "Scan Complete" appears.
6. Launch any calculated field in the opened workbook.
7. Move the cursor to the calculated field for which you want to display a new window and press the F3 key.
8. The target calculated field window will then be newly launched.
9. Please watch the video to see how it has been done so far.
https://youtu.be/7o7OjOqTC5A

## How to build app bundle for macOS

### With PyInstaller

**Prerequisites**:

- macOS
- Python 3.11+
- Xcode Command Line Tools

**Build command**:

```
make clean pyinstaller
```

The build produces `build/dist/Tableau-Calc-Viewer.app`.

**Characteristics of app bundle**:

- It takes a couple of seconds until the app window shows up.

- Privacy & Security distinguishes each build in "Accessibility", "Input Monitoring", and "Files and Folders".
- App Translocation - a macOS security mechanism turns off the auto workbook finder.

### Without PyInstaller

**Prerequisites**:

- Python 3.11+
- make
- Docker

**Build command**:

```
make clean zipapp app_bundle download_pypkg mkdmg
```

The build produces `build/Tableau-Calc-Viewer.dmg` that contains `Tableau-Calc-Viewer.app` and `python-3.*-macos*.pkg`.

**Characteristics of app bundle**:

- Python is required as runtime.
- The Internet connection is required to install dependencies that the app does not bundle.
- Xcode Command Line Tools may be required to install dependencies that the app does not bundle.
- App Translocation - a macOS security mechanism turns off the auto workbook finder.
