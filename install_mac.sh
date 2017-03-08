#!/bin/bash -ex

main() {
    install_framework SDL2 SDL2-2.0.5.dmg
    install_framework SDL2_image SDL2_image-2.0.1.dmg
    install_framework SDL2_mixer SDL2_mixer-2.0.1.dmg
    install_framework SDL2_ttf SDL2_ttf-2.0.14.dmg
}

install_framework() {
    local name=$1
    local dmg_file=$2
    if [ -f "/Library/Frameworks/$1.framework/$1" ]; then
        echo "$1 is already installed" >&2
        exit 0
    fi

    sudo hdiutil attach "$2"
    sudo cp -r "/Volumes/$1/$1.framework" /Library/Frameworks/
    sudo hdiutil detach "/Volumes/$1"

    echo "Installed framework:"
    find "/Library/Frameworks/$1.framework" | while read line; do
        ls -l "$line"
    done
}

main "$@"