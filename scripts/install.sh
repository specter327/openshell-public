#!/bin/bash

set -e


PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"


echo "Installing OpenShell Public"
echo "Project: $PROJECT_DIR"



echo "Installing Python dependencies..."

pip3 install \
    -r "$PROJECT_DIR/scripts/requirements.txt" \
    --break-system-packages



echo "Dependencies installed"



echo "Configuring PYTHONPATH..."

EXPORT_LINE="export PYTHONPATH=$PROJECT_DIR:\$PYTHONPATH"


if ! grep -Fxq "$EXPORT_LINE" ~/.bashrc
then
    echo "$EXPORT_LINE" >> ~/.bashrc
fi



echo "Reload shell or execute:"

echo "source ~/.bashrc"
source ~/.bashrc

echo "Installation completed"