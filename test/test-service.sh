#!/usr/bin/env sh

echo "Started test script."

# Start server (default)

python ../src/main.py >& /dev/null &
mypid=$!

# Running testcases

./test.sh a default
./test.sh b default
./test.sh c default

echo "End of script."

# End Server
kill $mypid