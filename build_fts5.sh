#!/bin/sh

HOME_DIR="$(pwd)"
OUTPUT_DIR="$1"

SQLITE_NAME="SQLite-release"
SQLITE_TGZ="$SQLITE_NAME.tgz" 

wget -c "www.sqlite.org/src/tarball/SQLite-release.tgz?uuid=release" -O $SQLITE_TGZ

tar -xzf $SQLITE_TGZ

cd "$SQLITE_NAME/" || exit

./configure && make "fts5.c"

cd "$HOME_DIR" || exit

case "$(uname)" in
    "Linux")
        gcc -g -fPIC -shared "$SQLITE_NAME/fts5.c" -o "$OUTPUT_DIR/fts5.so"
    ;;
    "Darwin")
        gcc -g -fPIC -shared "$SQLITE_NAME/fts5.c" -o "$OUTPUT_DIR/fts5.dylib"
    ;;
    *) exit
esac
