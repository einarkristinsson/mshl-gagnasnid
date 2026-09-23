#!/bin/bash
# deploy.sh — Gáttagægir á Cloud Run (Google Cloud), innan EES.
#
# Einu sinni, í eigin skel (þetta er innskráning og greiðslukort, ekki kóði):
#   gcloud auth login
#   gcloud config set project <verkefnis-auðkenni>     # verkefni með billing á
#
# Svo, hvenær sem er:
#   ./verkfaeri/gattagaegir/deploy.sh
#
# Byggir myndina úr Dockerfile í rót safnsins (Cloud Build), setur hana í loftið
# og prentar slóðina. Skalar í núll þegar enginn notar tólið.
set -euo pipefail
ROT="$(cd "$(dirname "$0")/../.." && pwd)"
NAFN="gattagaegir"
SVAEDI="${GCP_REGION:-europe-west4}"      # Holland — innan EES (samningur: ekki út fyrir EES)
VERKEFNI="${GCP_PROJECT:-$(gcloud config get-value project 2>/dev/null || true)}"

if [ -z "$VERKEFNI" ]; then
  echo "Ekkert Google Cloud-verkefni valið."
  echo "  gcloud config set project <auðkenni>   eða   GCP_PROJECT=<auðkenni> $0"
  exit 1
fi

echo "Verkefni: $VERKEFNI · svæði: $SVAEDI · þjónusta: $NAFN"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com --project "$VERKEFNI"

gcloud run deploy "$NAFN" \
  --source "$ROT" \
  --project "$VERKEFNI" \
  --region "$SVAEDI" \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 2 \
  --concurrency 4 \
  --cpu 1 \
  --memory 256Mi \
  --timeout 600 \
  --set-env-vars GATTAGAEGIR_OPINN=1

URL="$(gcloud run services describe "$NAFN" --project "$VERKEFNI" \
        --region "$SVAEDI" --format 'value(status.url)')"
echo
echo "Gáttagægir: $URL"
curl -s "$URL/api/heilsa"; echo
