#!/system/bin/sh
export PATH="/data/xbin:$PATH"
marvel='/data/data/com.marvel.unlimited'
local='/sdcard/comics'
db=`ls "$marvel/databases" | grep -E "^[0-9]+library\.sqlite$"`
mandb=`ls "$marvel/databases" | grep -E "^[0-9]+_manifest\.sqlite$"`
cd $local/sources

for f in *; do
    
    if [ -f "$f/cov.jpg" ]; then
        mv "$f/cov.jpg" "$local/sources/$f/00.jpg"
    fi
    cd "$local/sources/$f"
    count=`ls | wc -l`

    if [ "$count" -lt 5 ]; then
         cd ../
         rm -rf "$f"
    else
         for i in *; do
             echo `mv "$i" "0$i"`
         done
    
      cd "$local/sources"
      new=`sqlite3 "$local/$db" "Select title from book Where digital_id = $f"`
      
      if [ ! -f "$local/cbz/$new.cbz" ]; then
          zip "$f" "$f"/*
          mv "$f.zip" "$local/cbz/${f%.zip}.cbz" 
      else
         rm -rf $f;
      fi
    
      old=`sqlite3 "$marvel/databases/$mandb" "UPDATE manifest_issue SET offline = null WHERE id = $f"`

    fi
done
 
exit 0;
