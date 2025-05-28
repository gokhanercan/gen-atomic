#!/bin/bash
export PYTHONPATH=./src
uvicorn api.api:app --reload --reload-dir src --port 8510
read -rsp $'Press any key to continue...\n' -n1 key
#check http://127.0.0.1:8510/docs for the api documentation
