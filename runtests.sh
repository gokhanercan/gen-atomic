SCRIPT_DIR=$(dirname "$0")
echo "Script directory: $SCRIPT_DIR"
path=$SCRIPT_DIR\\TestsRunner.py
echo $path
python $path
read -rsp $'Press any key to continue...\n' -n1 key
