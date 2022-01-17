#!/bin/zsh
pyenv local 3.8.10
if [[ $(python3 --version) != *"3.8.10"* ]]; then
	echo "bad version"
	exit 5
else
	python3 -m venv venv
	source venv/bin/activate
	pip3 install --upgrade pip
	pip3 install wheel
	pip3 install -r all_requirements.txt
	exit 0
fi
