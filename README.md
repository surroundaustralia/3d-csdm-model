# 3D CSDM Ontologies â€“ OGC Blocks register

The ontology modules of the ICSM 3D Cadastral Survey Data Model (3D CSDM) from the
[`csdm_model`](https://github.com/icsm-au/3d-csdm/tree/main/csdm_model) directory of `icsm-au/3d-csdm`. They are packaged
as [OGC Blocks](https://ogcincubator.github.io/bblocks-docs/), with one block per ontology.

Identifier prefix: `icsm.csdm.`

The register is split in two:

- **`icsm.csdm.model.*` – the CSDM model.** The ontology modules and SHACL shapes that describe the CSDM, with the
  canonical examples for each module. These blocks do not depend on the utility blocks.
- **`icsm.csdm.utility.*` – design process and documentation.** The vocabularies, meta-models and evidence used to
  design and document the model: implementation-specification taxonomy, requirements meta-model, example-attachment
  shapes, attributions, implementation examples from existing formats, competency queries and the pyLODE
  configuration. These blocks depend on the model, not the other way round.

## Model blocks (`_sources/model/`)

| block | source ontology | shapes / examples | depends on (common ontologies) |
|---|---|---|---|
| `model.commonpatterns` | `commonpatterns.ttl` | commonpatterns shapes, 1 example, 2 fail tests | utility `compoundName.ontology` |
| `model.geometry` | `geometryprim.ttl` | geometryprimitives shapes, 1 example | cdm `geosparql`; topo `ogc.geo.topo.ontology`; land-parcels `spatialRepresentationDefinition` |
| `model.surveyfeatures` | `surveyfeats.ttl` | survey_features shapes, 2 examples | cdm `geosparql`, `prof`, `dcterms` |
| `model.surveyobs` | `surveyobs.ttl` | vector_observations shapes, 1 example | cdm `sosa`, `geosparql`, `schema-org`, `dcterms` |
| `model.surveyprov` | `surveyprov.ttl` | 1 example | cdm `prov`, `prof` |
| `model.container` | `container.ttl` | container shapes | cdm `sosa`, `prov`; skos `concept` |
| `model.all` | `csdm.ttl` (PROF profile of all modules) | – | `model.container`, `model.geometry` |

The Cadastral Parcels module has been replaced by OGC Land Parcels. `model.parcelsalignment` deprecates each CSDM
parcels term and maps it to the Land Parcels term that replaces it. The original module and its reconciliation are kept
for reference in `working/retired/parcels/`.

## Utility blocks (`_sources/utility/`)

| block | source | purpose | depends on |
|---|---|---|---|
| `utility.impspecs` | `impspecs.ttl`, speclist shapes | SKOS taxonomy of specifications used to classify implementation examples | skos `concept`, `conceptScheme`; cdm `dcterms`, `prov` |
| `utility.reqmetamodel` | `reqmetamodel.shapes.ttl` | links model elements to canonical and implementation examples | cdm `prof` |
| `utility.ontexamples` | `shapes_4_modelexamples.ttl` | PROF-based shapes for attaching examples to ontology classes | cdm `prof`, `prov`, `dcterms` |
| `utility.attributions` | `attributions.ttl` | persons and organisations credited for the CSDM | skos `conceptScheme` |
| `utility.evidence` | canonical example closure, implementation examples, competency SPARQL | evidence base for the design | `model.all`, `utility.impspecs`, `utility.reqmetamodel`, `utility.ontexamples` |
| `utility.modelindex` | `modelindex.ttl` | classification of model elements (`ModelledElement`, `ClassIn3DCadastre`, `StandardClass`, `GeoSPARQL-3D`) used to organise the documentation; moved from `container.ttl` | `model.all`, `model.commonpatterns` |
| `utility.documentation` | `pylode.ttl` | pyLODE configuration for the model documentation | `model.all`, `utility.attributions`, `utility.modelindex` |

In the model blocks, classes are linked to their canonical example instances with `skos:example` (formerly
`reqmetamodel:canonicalExample`). Links from model classes to implementation examples in other formats
(`reqmetamodel:implExample`) are kept only in `utility.evidence`, in the canonical example closure. The model sources
still carry some design-process references as plain IRIs, without a block dependency: the per-module examples import
the ontexamples shapes, and the `surveyfeats.ttl` ontology header has an `implExample` descriptor that conforms to
`impspecs` concepts.

Dependencies between the CSDM modules follow their (commented-out) `owl:imports` and the namespaces they actually use.
`cdm` = [Cross-domain model](https://ogcincubator.github.io/cross-domain-model/) (`ogc.model.cross-domain.*`),
`skos` = [SKOS blocks](https://ogcincubator.github.io/bblocks-skos/) (`ogc.skos.*`). SKOS is only listed where SKOS
classes are used in the model, not where SKOS is just used for annotation.

The Common Patterns module is not packaged here, and is split in two:

- **Compound names** (`CompoundName`, `NamePart`, `name`, `namePartType`, `namePartRef`) are reused from the OGC
  [Utility](https://ogcincubator.github.io/bblocks-utility/) register (unrelated to the CSDM `utility.*` blocks here)
  as `ogc.bbr.utils.compoundName.ontology`, in the `https://w3id.org/ogc/utils/label/` namespace (prefix `com:`).
- **The other common patterns** (`Measure`, `value`, `qualityMeasure`, `qualityClass`,
  `RelevantJurisdictionalCodelist`, `Report`, `Common`) are the `model.commonpatterns` block of this register, in the
  original `https://linked.data.gov.au/def/csdm/commonpatterns/` namespace (prefix `commonpatterns:`).

`surveyfeatures`, `surveyobs`, `surveyprov` and `container` depend on both.

The `geometry` module is mapped (`skos:closeMatch` / `skos:relatedMatch`) to the
[Topo-Feature](https://ogcincubator.github.io/topo-feature/) ontology (`ogc.geo.topo.ontology`), which defines the
topology terms of the exchange encoding, and to the Land Parcels spatial-representation ontology. It also absorbs the
former `model.geosparql3d` placeholder, which declared no terms of its own and is kept for reference in
`working/retired/geosparql3d/`.

These source files were not packaged:
- `manifest.ttl`: TopBraid EDG project configuration.
- `static/`: pre-generated HTML documentation.
- `.idea/`, `.project`, `build-local/`: tooling files.

## Reconciliation with OGC Land Parcels

`working/retired/parcels/description.md` compares the CSDM parcels ontology with the
[Land Parcels ontology](https://github.com/ogcincubator/bblocks-land-parcels/tree/master/_sources/ontology) concept by
concept, ignoring IRIs, and lists the points to resolve. The machine-readable form is in
`working/retired/parcels/reconciliation/differences.csv`. To regenerate it (requires `rdflib`):

```bash
tools/reconcile-parcels.sh
```

`tools/compare_ontologies.py` is generic and can be used to compare any other pair of modules.

## Changes made to the source files

- `utility/evidence/examples/canonical_examples_closure.ttl`: added the missing `.` after the `implext:` prefix declaration (the file
  did not parse).
- `model/surveyobs/examples/vector_observations_examples.ttl`: five observations used `sosa:phenomenomTime` with the invalid
  `xsd:date` `"14-01-2001"`. These are now `sosa:phenomenonTime` with `"2001-01-14"`.
- `model/surveyobs/examples/vector_observations_examples.ttl`: completed the occupation observations `oo1` and `oo11`.
  - Added a new `occupation_vector_observations` collection. Like the other collections in the file, it supplies the
    shared observed property (`surveyobs:VectorDetermination`), phenomenon time and sensor (`eq1`).
  - Gave `oo1` a `QualifiedVector` result. **Its values are illustrative** (and noted as such in the data) because the
    example coordinates are not mutually consistent: T2 to Occ10 is about 97 m from the coordinates, but `oo11` records
    2.14 m.
- `model/surveyobs/examples/vector_observations_examples.ttl`: `obs1` now uses `sosa:usedProcedure` in place of
  `sosa:Procedure`, which is a class, and `sosa:hasFeatureOfInterest` in place of `sosa:featureOfInterest`.
- `model/surveyobs/surveyobs.ttl`: made the same two fixes in the `skos:example` text of `surveyobs:SurveyVectorObservation`.
  The `skos:example` texts of `OccupationObservation` and `SurveyVectorObservation` now use the `surveyobs:` prefix in
  place of the old `surveylineobs:`.
- `model/surveyobs/vector_observations.shapes.ttl`: `:FeatureIsASurveyVector` now uses `sh:path sosa:hasFeatureOfInterest` in
  place of `sosa:featureOfInterest`.

- **Common Patterns split between the Utility register and this register:** compound name references use
  `https://w3id.org/ogc/utils/label/` (`ogc.bbr.utils.compoundName.ontology`); references to `Measure`,
  `qualityMeasure` and `RelevantJurisdictionalCodelist` use `https://linked.data.gov.au/def/csdm/commonpatterns/`
  (`model.commonpatterns`).
- **Meta-classes moved out of the container module:** `ModelledElement`, `ClassIn3DCadastre`, `StandardClass`,
  `GeoSPARQL-3D` and the axioms classifying model classes with them are now in `utility.modelindex` (IRIs unchanged).
  `surveyobs:Measure`, which `container.ttl` declared with the label "GeoSPARQL 1.2 (3D profile)", is now a deprecated
  equivalent of `commonpatterns:Measure`.
- **Geometry terms moved out of the GeoSPARQL and SKOS namespaces:** `geo:asGMLTopo`, `geo:extension`,
  `geo:isOutward`, `geo:touchesInward`, `geo:touchesOutward` and `skos:extrusion` are now `geometry:asGMLTopo` ...
  `geometry:extrusion`, in the ontology, shapes and examples. The broken `geometry:` / `geometr:` prefix declarations in
  `geometryprimitives_examples.ttl` now point to the geometry namespace.
- **Name parts in the examples rewritten to the compoundName JSON model.** The utility shapes follow that model. In
  `parcels/examples/parcel_examples.ttl`, `model/surveyfeatures/examples/survey_features_examples.ttl` and
  `model/surveyobs/examples/vector_observations_examples.ttl`:
  - the part label is `rdfs:label` (was `skos:prefLabel`);
  - the part type is `com:namePartType` with an IRI in the example namespace
    `https://linked.data.gov.au/def/csdm/examples/nameparttypes/` (was a literal `dct:type` or `dct:subject`);
  - T3's parts use `dct:hasPart` (was `http://purl.org/dc/elements/1.1/hasPart`).

## Known validation findings

All blocks pass validation, including against the SOSA SHACL rules inherited from `ogc.model.cross-domain.sosa`.

The property shape `:FeatureIsASurveyVector` in `vector_observations.shapes.ttl` is not used by any node shape, so it
has no effect on validation.

## Building locally

```bash
./build.sh   # outputs to build-local/, report in build-local/tests/report.html
./view.sh    # viewer on http://localhost:9090
```

### Until the new dependency blocks are published

`model.geometry` depends on `ogc.geo.topo.ontology` (Topo-Feature register), which is not published yet, so a build
against the published registers will report it as missing. To test against a local build, export the Topo-Feature
register with its public base URL and map it in the gitignored `bblocks-config-local.yml` (key `url-mappings`; an
`x-url-mappings` key is ignored) and `.volumes`. The postprocessor fetches and caches `@org/...` import aliases
*before* it applies `url-mappings`, so only full-URL imports (as used for Topo-Feature in `bblocks-config.yaml`) can be
redirected.
