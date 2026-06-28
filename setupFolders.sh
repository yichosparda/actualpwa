#!/bin/bash
set -euo pipefail


# Check if exactly two parameters were provided

if [ $# -ne 2 ]; then

    echo "Usage: $0 <source_folder> <destination_folder>"

    echo "  <source_folder> is the folder containing the files to be copied."

    echo "  <destination_folder> is the folder where the files will be copied."

    exit 1

fi



# Assign parameters to variables

SOURCE="$1"
DEST="$2"



# Verify that source folder exists

if [ ! -d "$SOURCE" ]; then

    echo "Error: Source folder '$SOURCE' does not exist."

    exit 1

fi



# Create the destination folder structure

mkdir -p "$DEST/static"

mkdir -p "$DEST/templates"



# Create app.py in the destination folder

touch "$DEST/app.py"



# Copy files from the source folder to the destination/static folder

cp "$SOURCE/style.css" "$DEST/static/"

cp "$SOURCE/script.js" "$DEST/static/"

cp "$SOURCE/swiper-bundle.min.css" "$DEST/static/"

cp "$SOURCE/swiper-bundle.min.js" "$DEST/static/"

cp "$SOURCE/favicon.ico" "$DEST/static/"

cp "$SOURCE/manifest.json" "$DEST/static/"

cp "$SOURCE/service-worker.js" "$DEST/static/"

cp -r "$SOURCE/Belanosima" "$DEST/static/"

cp -r "$SOURCE/icons" "$DEST/static/"

cp -r "$SOURCE/items" "$DEST/static/"

cp -r "$SOURCE/Kantumruy_Pro" "$DEST/static/"

cp "$SOURCE/bakery.png" "$DEST/static/"

cp "$SOURCE/carousel-home.js" "$DEST/static/"

cp "$SOURCE/carousel-menu.js" "$DEST/static/"

cp "$SOURCE/contact.png" "$DEST/static/"

cp "$SOURCE/cover.png" "$DEST/static/"

cp "$SOURCE/front.png" "$DEST/static/"

cp "$SOURCE/logo.png" "$DEST/static/"

cp "$SOURCE/index.html" "$DEST/templates/"

cp "$SOURCE/cart.html" "$DEST/templates/"

cp "$SOURCE/custom.html" "$DEST/templates/"

cp "$SOURCE/login.html" "$DEST/templates/"

cp "$SOURCE/menu.html" "$DEST/templates/"

cp "$SOURCE/product.html" "$DEST/templates/"

cp "$SOURCE/signup.html" "$DEST/templates/"


echo "Files have been successfully copied from '$SOURCE' to '$DEST'."