#!/bin/bash
# Regenerate the OWL consistency shapes (owl-consistency.shapes.ttl) of each CSDM model block from its ontology.
set -e
cd "$(dirname "$0")/.."
for pair in commonpatterns:commonpatterns.ttl geopose:geopose.ttl geometry:geometryprim.ttl \
            container:container.ttl surveyfeatures:surveyfeats.ttl surveyobs:surveyobs.ttl; do
  block=${pair%%:*}; ont=${pair#*:}
  python tools/owl2shacl.py "_sources/model/$block/$ont" "_sources/model/$block/owl-consistency.shapes.ttl"
done

# Explicit class targets for the hand-written model shapes (see tools/shape-targets.py)
python tools/shape-targets.py "_sources/**/*.ttl" \
  _sources/model/commonpatterns/shapes.shacl _sources/model/container/container.shapes.ttl \
  _sources/model/geometry/geometryprimitives.shapes.ttl _sources/model/surveyfeatures/survey_features.shapes.ttl \
  _sources/model/surveyobs/vector_observations.shapes.ttl
