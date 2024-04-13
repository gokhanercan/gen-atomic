SCRIPT_DIR=$(dirname "$0")
echo "Script directory: $SCRIPT_DIR"
path=$SCRIPT_DIR
echo $path
pytest $path --collect-only -v
read -rsp $'Press any key to continue...\n' -n1 key
