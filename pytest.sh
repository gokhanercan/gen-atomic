SCRIPT_DIR=$(dirname "$0")
echo "Script directory: $SCRIPT_DIR"
path=$SCRIPT_DIR
echo $path
pytest $path -v
read -rsp $'Press any key to continue...\n' -n1 key

#To watch pytests continuously
 #pip install pytest-watch
 #ptw --clear