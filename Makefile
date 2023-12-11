
PYTHON=python3
NAME=Tableau-Calc-Viewer
MAIN=main:main
PYPKG=https://www.python.org/ftp/python/3.11.6/python-3.11.6-macos11.pkg

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

.PHONY: contents
contents:
	mkdir -p /tmp/dmg/$(NAME).app/Contents
	echo 'FEYEtcav' > /tmp/dmg/$(NAME).app/Contents/PkgInfo
	cp /project/resources/Info.plist /tmp/dmg/$(NAME).app/Contents/Info.plist

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
