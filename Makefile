
PYTHON=python3
BUILD_DIR=build
NAME=Tableau-Calc-Viewer

SCRIPTNAME=src/main.py
ifeq ($(shell ${PYTHON} -c "import platform; print(platform.system())"), Windows)
	VENV_PYTHON = $(BUILD_DIR)\venv\Scripts\python -E
else
	VENV_PYTHON = $(BUILD_DIR)/venv/bin/python -E
endif

SIGN=tcav
MAIN=main:main
PYPKG=https://www.python.org/ftp/python/3.11.7/python-3.11.7-macos11.pkg

define INFO_PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleDevelopmentRegion</key>
  <string>English</string>

  <key>CFBundleExecutable</key>
  <string>$(NAME).command</string>

  <key>CFBundleIdentifier</key>
  <string>com.ferveyes.$(NAME)</string>

  <key>CFBundleInfoDictionaryVersion</key>
  <string>6.0</string>

  <key>CFBundlePackageType</key>
  <string>FEYE</string>

  <key>CFBundleSignature</key>
  <string>$(SIGN)</string>

  <key>CFBundleSupportedPlatforms</key>
  <array>
    <string>MacOSX</string>
  </array>

  <key>LSEnvironment</key>
  <dict>
    <key>PATH</key>
    <string>/Library/Frameworks/Python.framework/Versions/3.19/bin:/Library/Frameworks/Python.framework/Versions/3.18/bin:/Library/Frameworks/Python.framework/Versions/3.17/bin:/Library/Frameworks/Python.framework/Versions/3.16/bin:/Library/Frameworks/Python.framework/Versions/3.15/bin:/Library/Frameworks/Python.framework/Versions/3.14/bin:/Library/Frameworks/Python.framework/Versions/3.13/bin:/Library/Frameworks/Python.framework/Versions/3.12/bin:/Library/Frameworks/Python.framework/Versions/3.11/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
  </dict>
</dict>
</plist>
endef

RM_RF=$(PYTHON) -c "__import__('shutil').rmtree(__import__('sys').argv[1], ignore_errors=True)"
CP=$(PYTHON) -c "__import__('shutil').copy(*__import__('sys').argv[1:])"
PRINTENV=$(PYTHON) -c "print(__import__('os').environ[__import__('sys').argv[1]])"
MKDIR_P=$(PYTHON) -c "__import__('os').makedirs(__import__('sys').argv[1], exist_ok=True)"
DOWNLOAD=$(PYTHON) -c "__import__('urllib.request').request.urlretrieve(*__import__('sys').argv[1:])"

.PHONY: clean
clean:
	$(RM_RF) $(BUILD_DIR)

.PHONY: zipapp
zipapp:
	$(MKDIR_P) $(BUILD_DIR)/zipapp
	$(PYTHON) -m pip --disable-pip-version-check install --no-user --no-deps --target build/zipapp .
	$(PYTHON) -m pip --disable-pip-version-check install --no-user --no-deps --target build/zipapp -r requirements-zipapp.txt
	$(PYTHON) -m zipapp --python "/usr/bin/env python3" --main "$(MAIN)" --output build/$(NAME).pyz build/zipapp

export INFO_PLIST
.PHONY: app_bundle
app_bundle:
	$(MKDIR_P) $(BUILD_DIR)/dist/$(NAME).app/Contents/MacOS
	echo FEYE$(SIGN)>$(BUILD_DIR)/dist/$(NAME).app/Contents/PkgInfo
	$(PRINTENV) INFO_PLIST>$(BUILD_DIR)/dist/$(NAME).app/Contents/Info.plist
	$(CP) $(BUILD_DIR)/$(NAME).pyz $(BUILD_DIR)/dist/$(NAME).app/Contents/MacOS/$(NAME).command

.PHONY: download_pypkg
download_pypkg:
	$(DOWNLOAD) $(PYPKG) $(BUILD_DIR)/$(notdir $(PYPKG))

.PHONY: mkdmg
mkdmg:
	docker run -it -v "${CURDIR}:/work" -w /work --entrypoint /usr/bin/make sporsh/create-dmg createdmg

.PHONY: createdmg
createdmg:
	mkdir -p /tmp/dmg/
	cp /work/$(BUILD_DIR)/*.pkg /tmp/dmg/
	cp -R /work/$(BUILD_DIR)/dist/$(NAME).app /tmp/dmg/
	chmod +x /tmp/dmg/$(NAME).app/Contents/MacOS/*
	bash /create-dmg.sh "$(NAME)" /tmp/dmg /work/$(BUILD_DIR)/$(NAME).dmg

.PHONY: pyinstaller
pyinstaller:
	$(MKDIR_P) $(BUILD_DIR)/venv
	$(PYTHON) -m venv $(BUILD_DIR)/venv
	$(VENV_PYTHON) -m pip --disable-pip-version-check install .
	$(VENV_PYTHON) -m pip --disable-pip-version-check install -r requirements.txt
	$(VENV_PYTHON) -m pip --disable-pip-version-check install pyinstaller
	$(VENV_PYTHON) -m PyInstaller --distpath $(BUILD_DIR)/dist --name $(NAME) --onefile --noconsole --noconfirm --osx-bundle-identifier com.ferveyes.$(NAME) $(SCRIPTNAME)
