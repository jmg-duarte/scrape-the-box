#!/usr/bin/sh

HOME_DIR="$(pwd)"
OUTPUT_DIR="$HOME_DIR"

SQLITE_NAME="SQLite-release"
SQLITE_TGZ="$SQLITE_NAME.tgz" 

/usr/bin/wget -c "https://www.sqlite.org/src/tarball/SQLite-release.tgz?uuid=release" -O $SQLITE_TGZ

/usr/bin/tar -xzf $SQLITE_TGZ

cd "$SQLITE_NAME/" || exit

./configure && /usr/bin/make "fts5.c"

cd "$HOME_DIR" || exit

STB_LIB="/usr/local/lib/stb"

/usr/bin/sudo /usr/bin/mkdir "$STB_LIB"

case "$(uname)" in
    "Linux")
        OUT_LIB="fts5.so"
        /usr/bin/gcc -g -fPIC -shared "$SQLITE_NAME/fts5.c" -o "$OUTPUT_DIR/$OUT_LIB"
        /usr/bin/sudo /usr/bin/mv "$OUTPUT_DIR/$OUT_LIB" "$STB_LIB/$OUT_LIB"
    ;;
    "Darwin")
        OUT_LIB="fts5.dylib"
        /usr/bin/gcc -g -fPIC -shared "$SQLITE_NAME/fts5.c" -o "$OUTPUT_DIR/$OUT_LIB"
        /usr/bin/sudo /usr/bin/mv "$OUTPUT_DIR/$OUT_LIB" "$STB_LIB/$OUT_LIB"
    ;;
    *) exit
esac
