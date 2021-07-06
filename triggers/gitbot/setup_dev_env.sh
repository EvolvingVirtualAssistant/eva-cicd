#!/usr/bin/env bash

echo "Starting setup of E.V.A CI/CD git-bot development environment"

function get_current_os() {
    case "$OSTYPE" in
    darwin*)
        echo "OSX - not supported"
        exit 1
        ;;
    linux*)
        os="LINUX"
        ;;
    msys*)
        os="WINDOWS"
        ;;
    *)
        echo "unknown: $OSTYPE - not supported"
        exit 1
        ;;
    esac

    echo "Current OS: $os"
}

function install_python() {
    ## Checks if python is installed
    if ! [ -x "$(command -v python)" ]; then
        echo 'Warn: python is not installed.' >&2
        echo "Trying to install python"
        if [ $os == "WINDOWS" ]; then
            choco install python3
        elif [ $os == "LINUX" ]; then
            sudo apt-get update
            sudo apt-get install python3 python3-pip
        fi
    else
        ## Upgrades python
        echo "Trying to upgrade python"
        if [ $os == "WINDOWS" ]; then
            choco upgrade python3
        elif [ $os == "LINUX" ]; then
            sudo apt-get update
            sudo apt-get install python3 python3-pip
        fi
    fi

    ## Prints python version
    if [ $os == "WINDOWS" ]; then
        python --version
    elif [ $os == "LINUX" ]; then
        python3 --version
    fi
}

function install_requirements() {
    pip install -r dev-requirements
}

function print_notes() {
    if [ $os == "WINDOWS" ]; then
        echo "On vscode if libraries are not recognized go to File > Preferences > Settings > Search for interpreter > Select python > Set 'py' as the default one, instead of 'python'."
    fi
}

## Install required softwared

get_current_os

install_python

install_requirements

print_notes

echo "Instalation done. Happy coding!!!"
