echo "Uninstalling: OpenShell Public...";

echo "Uninstalling Python dependencies...";
pip3 uninstall -r requirements.txt -y --break-system-packages;

echo "Python dependencies uninstalled";

echo "Uninstall completed";