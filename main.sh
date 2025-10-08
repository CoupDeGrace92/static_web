#Exit immediately if any command exits with non-zero status, treat unset variables as an error, in a pipeline of variables, return the first failing exit code, not just the last
#set -euo pipefail

#If one is set (the dash), and is --clear, clear the terminal
#if [ "${1-}" = "--clear" ]; then
#    clear
#fi

python3 src/main.py