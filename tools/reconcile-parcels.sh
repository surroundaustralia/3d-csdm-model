#!/bin/bash
# Re-generate the concept-level comparison between the CSDM parcels ontology and the
# OGC Land Parcels ontology (ignoring namespace IRIs).
#   LAND_PARCELS: path or URL of the land-parcels ontology (default: published source on GitHub)
set -e
cd "$(dirname "$0")/.."
LAND_PARCELS=${LAND_PARCELS:-https://raw.githubusercontent.com/ogcincubator/bblocks-land-parcels/master/_sources/ontology/parcels.ttl}
python tools/compare_ontologies.py working/retired/parcels/parcels.ttl "$LAND_PARCELS" \
  --source-label CSDM --target-label land-parcels \
  --map parcel=https://linked.data.gov.au/def/csdm/parcels/,https://w3id.org/ogc/ladm/parcels/ \
  --map com=https://w3id.org/ogc/utils/label/,https://w3id.org/ogc/utils/label/ \
  --map commonpatterns=https://linked.data.gov.au/def/csdm/commonpatterns/,https://linked.data.gov.au/def/csdm/commonpatterns/ \
  --map geometry=https://linked.data.gov.au/def/csdm/geometry/,https://linked.data.gov.au/def/csdm/geometry/ \
  --ont https://linked.data.gov.au/def/csdm/parcels,https://w3id.org/ogc/ladm/parcels \
  --md working/retired/parcels/reconciliation/differences.md \
  --csv working/retired/parcels/reconciliation/differences.csv
