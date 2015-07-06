#!/system/bin/sh

marvel='/data/data/com.marvel.unlimited'
local='/sdcard/comics'
db=`ls "$marvel/databases" | grep -E "^[0-9]+library\.sqlite$"`

a="$1"
j
if [ $a == 1 ]; then
    chown -R u0_a207:u0_a210 $marvel
    chmod -R 777 $marvel
    exit 0
elif [ $a == 0 ]; then
    chown -R u0_a207:u0_a207 $marvel
    exit 0
else  
    exit 1
fi