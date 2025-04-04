#!/usr/bin/env bash
# Script: build_and_push_all.sh
# Purpose: Build and push multiple base Docker images, then build downstream images
# Usage: ./build_and_push_all.sh <USERNAME> <PASSWORD> [REGISTRY] [NAMESPACE] [PROJECT]

set -euo pipefail

# Move up one directory from where the script is located
cd "$(dirname "${BASH_SOURCE[0]}")/../src"

#####################################
# 1. PARSE ARGUMENTS
#####################################

# We expect at least two arguments: username and password.
# We optionally allow three more: registry, namespace, and project.
# If not provided, fallback to environment variables or defaults.

if [ $# -lt 2 ]; then
  echo "Usage: $0 <USERNAME> <PASSWORD> [REGISTRY] [NAMESPACE] [PROJECT]"
  exit 1
fi

# Mandatory arguments
USERNAME="$1"
PASSWORD="$2"

# Optional arguments with fallbacks
CI_REGISTRY="${3:-${CI_REGISTRY:-registry.wildfireworkspace.com}}"
CI_PROJECT_NAMESPACE="${4:-${CI_PROJECT_NAMESPACE:-eop}}"
CI_PROJECT_NAME="${5:-${CI_PROJECT_NAME:-streamlit-1.0}}"

#####################################
# 2. CONFIGURATION
#####################################

# Full registry path (e.g., registry.gitlab.com/my-group/my-project)
REGISTRY_PATH="${CI_REGISTRY}/${CI_PROJECT_NAMESPACE}/${CI_PROJECT_NAME}"

# Define the Dockerfiles for your base images and your downstream images.
# Format: "image_name Dockerfile_path"
BASE_IMAGES=(
  "default-base DEFAULT_BASE_IMAGE/Dockerfile"
  "toolbox-base ../Dockerfile-base"
  "diarization-base data_toolbox/diarization/Dockerfile-base"
  "diarization_api-base data_toolbox/diarization/api/Dockerfile-base"
  "hijri_calendar_converter-base data_toolbox/hijri_calendar_converter/Dockerfile-base"
  "hijri_calendar_converter_api-base data_toolbox/hijri_calendar_converter/api/Dockerfile-base"
  "text_extractor-base data_toolbox/text_extractor/Dockerfile-base"
  "image_to_text-base data_toolbox/image_to_text/Dockerfile-base"
  "arab_dialect_id-base data_toolbox/arab_dialect_id/Dockerfile-base"
  "cem_search-base data_toolbox/cem_search/Dockerfile-base"
  "image_triage-base data_toolbox/image_triage/Dockerfile-base"
  "cure-base data_toolbox/cure/Dockerfile-base"
  "cure_api-base data_toolbox/cure/api/Dockerfile-base"
)

#####################################
# 3. DOCKER LOGIN
#####################################
echo "==> Logging in to Docker registry: ${CI_REGISTRY}"
echo "$2" | docker login "${CI_REGISTRY}" -u "$1" --password-stdin

#####################################
# 4. FUNCTION TO BUILD AND PUSH
#####################################
build_and_push() {
  local image_name="$1"
  local dockerfile="$2"

  echo "==> Building image '${image_name}' using Dockerfile: '${dockerfile}'"
  docker build -t "${REGISTRY_PATH}/${image_name}:latest" -f "${dockerfile}" .

  echo "==> Pushing image '${image_name}' to ${REGISTRY_PATH}/${image_name}:latest"
  docker push "${REGISTRY_PATH}/${image_name}:latest"

  echo "==> Finished building and pushing '${image_name}' tag 'latest'"
  echo
}

#####################################
# 5. BUILD & PUSH BASE IMAGES
#####################################
echo "==> Building and pushing base images..."
for base in "${BASE_IMAGES[@]}"; do
  # Split the string into two parts: <image_name> <dockerfile>
  IFS=" " read -r NAME DOCKERFILE <<< "$base"
  build_and_push "${NAME}" "${DOCKERFILE}"
done

echo "==> All images built and pushed successfully!"