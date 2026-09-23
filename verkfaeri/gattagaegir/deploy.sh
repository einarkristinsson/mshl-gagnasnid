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

# Geymslan sem „deploy --source" setur myndina í. Stofnuð hér, ekki látin
# gcloud um það, því heimildin á Artifact Registry er ekki komin í gegn fyrstu
# sekúndurnar eftir að kveikt er á þjónustunni: mælt 23.9 — PERMISSION_DENIED
# strax á eftir enable, sama skipun gekk tveimur mínútum síðar. Reynt þar til
# hún svarar, mest tvær mínútur.
GEYMSLA="cloud-run-source-deploy"
for i in $(seq 1 12); do
  if gcloud artifacts repositories describe "$GEYMSLA" --location "$SVAEDI" \
       --project "$VERKEFNI" >/dev/null 2>&1; then break; fi
  if gcloud artifacts repositories create "$GEYMSLA" --repository-format docker \
       --location "$SVAEDI" --project "$VERKEFNI" >/dev/null 2>&1; then
    echo "Geymsla $GEYMSLA stofnuð í $SVAEDI"; break
  fi
  echo "  bíð eftir Artifact Registry-heimild ($i/12) …"; sleep 10
done

# Cloud Build byggir myndina sem sjálfgefni Compute-þjónustureikningurinn, og
# í nýjum verkefnum (frá 2024) hefur hann engin hlutverk. Skjölin
# (docs.cloud.google.com/run/docs/deploying-source-code) segja roles/run.builder.
# Mælt 23.9: án þess fellur byggingin á „default service account is missing
# required IAM permissions". Endurtekin veiting er skaðlaus.
NUMER="$(gcloud projects describe "$VERKEFNI" --format 'value(projectNumber)')"
gcloud projects add-iam-policy-binding "$VERKEFNI" \
  --member "serviceAccount:${NUMER}-compute@developer.gserviceaccount.com" \
  --role roles/run.builder --condition None >/dev/null

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
