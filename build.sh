#!/bin/bash


# this script manages this project by building pydocs, uploading to pypi
# and compiling the source

# set python version
PY=python3
# get version of package
# combine with name to get filenames
V="$($PY setup.py -V)"
TO="release"
NAME="hashit-${V}"
ZIP="dist/${NAME}.zip"
TAR="dist/${NAME}.tar"

if [ "$1" == "docs" ]
then
    # build docs using pydoc
    $PY -m pydoc -w hashit
    $PY -m pydoc -w hashit.__main__
    $PY -m pydoc -w hashit.detection
    $PY -m pydoc -w hashit.extra
    $PY -m pydoc -w hashit.version
    mv *.html ./docs/pydocs
    #cd ./docs/pydocs
    #find . -name "*.ht*" | while read i; do pandoc -f html -t markdown "$i" -o "${i%.*}.md"; done
    #cd ../..
    # clean/create file
    echo -e "---\nlayout: default\n---\n" > ./docs/pydoc.md
    $PY -c "from pydocmd.__main__ import main; import sys; sys.argv = ['', 'simple', 'hashit+', 'hashit.__main__+', 'hashit.detection+', 'hashit.extra+']; main()" >> ./docs/pydoc.md
    printf "\n\n[back](README.md)" >> ./docs/pydoc.md # add back button
    
    # push new documentation to wiki
    cp ./docs/*.md ../hashit.wiki
    mv ../hashit.wiki/index.md ../hashit.wiki/Home.md
    cd ../hashit.wiki
    # remove layout
    sed -i '/layout: default/d' *.md
    sed -i '/---/d' *.md
    # push to git
    sudo git add .
    sudo git commit -m "Updated wiki"
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


if [ "$1" == "upload" ]
then
    $PY setup.py sdist upload
    rm -rf ./dist
else
    # Move and print messages
    SILENT="$($PY setup.py sdist --quiet --formats zip,tar)"
    echo "Version, $V at $ZIP and $TAR"
    mv $ZIP "${TO}/hashit.zip"
    mv $TAR "${TO}/hashit.tar"
    echo "Moved to ${TO}/hashit.zip and ${TO}/hashit.tar"
    rm -r dist/

    if [ "$1" == "deb" ]
    then
        cd release
        rm -rf deb_dist
        py2dsc-deb hashit.zip
        exit
    fi
fi