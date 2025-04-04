#!/bin/bash

# Script to load all tarball Docker images in a directory into Docker

# Check if the directory argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory-containing-tarballs>"
    exit 1
fi

# Get the directory containing tarball images
DIR="$1"

# Check if the provided path is a directory
if [ ! -d "$DIR" ]; then
    echo "Error: '$DIR' is not a directory."
    exit 2
fi

# Iterate over all .tar files in the directory
for IMAGE in "$DIR"/*.tar; do
    # Check if there are any .tar files
    if [ ! -e "$IMAGE" ]; then
        echo "No .tar files found in $DIR."
        exit 3
    fi

    echo "Loading image: $IMAGE"
    docker load < "$IMAGE"

    # Check if the load command was successful
    if [ $? -ne 0 ]; then
        echo "Error loading image: $IMAGE"
    else
        echo "Successfully loaded: $IMAGE"
    fi
done

echo "All Docker images in $DIR have been loaded."
