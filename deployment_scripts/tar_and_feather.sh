#!/bin/bash

# List of Docker images
images=(
  "datatoolbox-v1.3.0"
  "streamlit-10-diarization"
  "streamlit-10-diarization_api"
  "streamlit-10-hijri_calendar_converter"
  "streamlit-10-hijri_calendar_converter_api"
  "streamlit-10-text_extractor"
  "streamlit-10-image_to_text"
  "streamlit-10-arab_dialect_id"
  "streamlit-10-cem_search"
  "streamlit-10-image_triage"
  "streamlit-10-cure"
  "streamlit-10-cure_api"
)

# Directory to save tarballs
output_dir="/data/move-to-g"
mkdir -p "$output_dir"

# Save each Docker image as a tarball
for image in "${images[@]}"; do
  echo "Saving image: $image"
  tarball_name="$output_dir/${image}.tar"
  docker save -o "$tarball_name" "$image"
  if [[ $? -eq 0 ]]; then
    echo "Saved $image to $tarball_name"
  else
    echo "Failed to save $image. Please ensure the image exists locally."
  fi
done

echo "All Docker images have been processed. Tarballs are located in $output_dir."
