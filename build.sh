#!/bin/bash

# in here all the tools for this project is automatazied

# this script manages this project by building pydocs, uploading to pypi
# and compiling the source running tests pushing to launchpad and more

# set python version
PY=python3
# get version of package
# combine with name to get filenames
V="$($PY setup.py -V)"
TO="release"
NAME="hashit-${V}"
ZIP="dist/${NAME}.zip"
TAR="dist/${NAME}.tar.gz"

if [ "$1" == "docs" ]
then
    # build docs using pydoc
    $PY -m pydoc -w hashit
    $PY -m pydoc -w hashit.__main__
    $PY -m pydoc -w hashit.detection
    $PY -m pydoc -w hashit.extra
    $PY -m pydoc -w hashit.version
    mv -f *.html ./docs/pydocs
    #cd ./docs/pydocs
    #find . -name "*.ht*" | while read i; do pandoc -f html -t markdown "$i" -o "${i%.*}.md"; done
    #cd ../..
    # clean/create file
    echo -e "---\nlayout: default\n---\n" > ./docs/pydoc.md
    $PY -c "from pydocmd.__main__ import main; import sys; sys.argv = ['', 'simple', 'hashit+', 'hashit.__main__+', 'hashit.detection+', 'hashit.extra+']; main()" >> ./docs/pydoc.md
    printf "\n\n[back](index.md)" >> ./docs/pydoc.md # add back button

    # push new documentation to wiki
    sudo cp ./docs/*.md ../hashit.wiki
    sudo mv ../hashit.wiki/index.md ../hashit.wiki/Home.md
    cd ../hashit.wiki
    # remove layout
    sudo chmod 777 *.md
    sudo sed -i '/layout: default/d' *.md
    sudo sed -i '/---/d' *.md
    sudo sed -e 's/\.md//g' -i *.md
    # push to git
    sudo git add .
    sudo git commit -m "Updated wiki"
    exit
fi

if [ "$1" == "push" ]
then
    echo push hashit
    git push origin master
    git push launchpad master
    cd ../hashit.wiki
    echo "PUSH wiki"
    sudo git push
    exit
fi

if [ "$1" == "install" ]
then
    $PY setup.py install
    rm -rf ./dist
    exit
fi


if [ "$1" == "test" ]
then
    python3 setup.py test
    python setup.py test
    rm */*.pyc # remove .pyc files from python2
    # and exit
    exit
fi

if [ "$1" == "clean" ]
then
    if [ -d "hashit.egg-info" ]
    then
        rm -rf "hashit.egg-info"
        echo "Removed egg-info"
    fi

    if [ -d "dist" ]
    then
        rm -rf "dist"
        echo "Removed dist"
    fi

    if [ -d "build" ]
    then
        rm -rf "build"
        echo "Removed build"
    fi

    if [ -d "release/deb_dist" ]
    then
        rm -rf "release/deb_dist"
        echo "Removed deb_dist"
    fi

    exit
fi


if [ "$1" == "upload" ]
then
    $PY setup.py sdist upload
    rm -rf ./dist
else
    # Move and print messages
    SILENT="$($PY setup.py sdist --quiet --formats zip,gztar)"
    echo "Version, $V at $ZIP and $TAR"
    mv $ZIP "${TO}/hashit.zip"
    mv $TAR "${TO}/hashit.tar.gz"
    echo "Moved to ${TO}/hashit.zip and ${TO}/hashit.tar.gz"
    rm -r dist/

    if [ "$1" == "deb" ]
    then
        cd release
        rm -rf deb_dist
        py2dsc-deb hashit.zip
        cd deb_dist
        
        # for launchpad dailybuilds
	    git init
	    # add remote and force push deb package
	    git remote add origin git+ssh://javadsm@git.launchpad.net/python3-hashit
	    git add . # add all files
	    git commit -m "DEB DIST BRANCH"
	    git push --force --set-upstream origin master
        # delete tmp files
        read -p "Delete deb_dist (y/n)?" choice
        case "$choice" in 
            y|Y ) rm -rf deb_dist;;
            n|N ) exit;;
            * ) echo exit;;
        esac
        # exit
        exit
    fi
    # exit
    exit
fi
