#!/system/bin/sh
db=`ls /sdcard/comics | grep -E "^[0-9]+library\.sqlite$"`

rm -rf /sdcard/comics/sources
rm -f "/sdcard/comics/$db"

if [ ! -d /sdcard/comics/sources ]; then
    mkdir /sdcard/comics/sources
fi

chmod -R 777 /sdcard/comics

exit 0;