
PYTHON=python3
NAME=Tableau-Calc-Viewer
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

.PHONY: clean 
clean:
	rmdir /q /s build >NUL || exit /b 0

.PHONY: appdir 
appdir:
	mkdir build\app

.PHONY: bdist_wheel
bdist_wheel:
	$(PYTHON) setup.py bdist_wheel --dist-dir build

.PHONY: install_requirements
install_requirements:
	$(PYTHON) -m pip --disable-pip-version-check install -r requirements.txt --no-deps --no-user --target build\app

.PHONY: installt_wheel
installt_wheel:
	$(PYTHON) -m pip --disable-pip-version-check install --no-index --find-links build --no-user --target build\app $(NAME)

.PHONY: zipapp
zipapp:
	$(PYTHON) -m zipapp --python "/usr/bin/env python3" --main "$(MAIN)" --output build\$(NAME).pyz build\app

.PHONY: download_pypkg
download_pypkg:
	pushd build && curl -O $(PYPKG) && popd

.PHONY: docker_createdmg
docker_createdmg:
	docker run -it -v "${CURDIR}:/project" -w /project --entrypoint /usr/bin/make sporsh/create-dmg createdmg

.PHONY: dmgdir
dmgdir:
	mkdir -p /tmp/dmg

export INFO_PLIST
.PHONY: contents
contents:
	mkdir -p /tmp/dmg/$(NAME).app/Contents
	echo 'FEYE$(SIGN)' > /tmp/dmg/$(NAME).app/Contents/PkgInfo
	echo "$$INFO_PLIST" > /tmp/dmg/$(NAME).app/Contents/Info.plist

.PHONY: macos
macos:
	mkdir -p /tmp/dmg/$(NAME).app/Contents/MacOS
	cp /project/build/$(NAME).pyz /tmp/dmg/$(NAME).app/Contents/MacOS/$(NAME).command
	chmod +x /tmp/dmg/$(NAME).app/Contents/MacOS/*.command

.PHONY: run_createdmg
run_createdmg:
	cp /project/build/*.pkg /tmp/dmg/
	bash /create-dmg.sh "$(NAME)" /tmp/dmg /project/build/$(NAME).dmg

build: appdir bdist_wheel install_requirements installt_wheel zipapp
dmg: download_pypkg docker_createdmg
createdmg: dmgdir contents macos run_createdmg
