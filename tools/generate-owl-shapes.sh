#!/bin/bash
# Regenerate the OWL consistency shapes (owl-consistency.shapes.ttl) of each CSDM model block from its ontology.
set -e
cd "$(dirname "$0")/.."
for pair in commonpatterns:commonpatterns.ttl geopose:geopose.ttl geometry:geometryprim.ttl \
            container:container.ttl surveyfeatures:surveyfeats.ttl surveyobs:surveyobs.ttl; do
  block=${pair%%:*}; ont=${pair#*:}
  python tools/owl2shacl.py "_sources/model/$block/$ont" "_sources/model/$block/owl-consistency.shapes.ttl"
done
