#!/system/bin/sh

marvel='/data/data/com.marvel.unlimited'
local='/sdcard/comics'
db=`ls "$marvel/databases" | grep -E "^[0-9]+library\.sqlite$"`

cp "$marvel/databases/$db" "$local/"
cp -R $marvel/files/reader/pages/* "$local/sources"

exit 0;