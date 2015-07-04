#!/system/bin/sh
export PATH="/data/xbin:$PATH"
marvel='/data/data/com.marvel.unlimited'
db=`ls "$marvel/databases" | grep -E "^[0-9]+library\.sqlite$"`

sqlite3 "$marvel/databases/$db" "UPDATE book SET in_library = '0' WHERE in_library = '1'"

rm -rf "$marvel"/files/reader/pages/*

exit 0