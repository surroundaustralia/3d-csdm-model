# CSDM ontology alignment with 3d-csdm-common: proposed changes

**Status:** proposal for review. Partly implemented on 2026-10-30; see section 12.
**Date:** 2026-10-30
**Scope:** the ontology blocks in this repository (`icsm.csdm.model.*`), and the component ontologies the CSDM
depends on: Land Parcels, Topo-Feature, SOSA (ogcapi-sosa) and Common Patterns / compoundName (bblocks-utility).

## 1. Purpose

The ontologies in this repository come from the earlier `icsm-au/3d-csdm` `csdm_model` phase. The JSON exchange
model in `3d-csdm-common`, the ICSM profile and the WA profile have moved on since then. This report:

- lists the terms the current JSON-LD bindings produce that no ontology defines;
- lists ontology definitions that conflict with how the schema actually uses a term;
- proposes changes to each ontology module, and identifies new ontology blocks and refactorings that are needed;
- keeps every existing JSON-LD binding working. **No IRI that any context binds to is renamed or removed.**

## 2. Sources examined

| Source | Location | Version used |
|---|---|---|
| CSDM ontologies (this repo) | `_sources/model/*`, `working/parcels` | working tree, 2026-10-30 |
| 3D CSDM common schema | `ngsc/3d-csdm-common` (surroundaustralia) | `main`, 2026-10-28 |
| ICSM profile | `ngsc/3d-csdm-profile-icsm` | 2026-10-27 |
| WA profile and documentation | `ngsc/3d-csdm-profile-wa` (`documents/`, `proposals/`) | 2026-10-30 |
| Land Parcels | `ngsc/bblocks-land-parcels` | 2026-10-26 |
| Topo-Feature | `ngsc/topo-feature` | 2026-09-23 |
| SOSA blocks | `ogc/ogcapi-sosa` | 2026-10-28 |
| Common Patterns / compoundName | `ngsc/bblocks-utility` | `master`, 2026-10-26 |

The older `icsm/3d-csdm-common` and `icsm/3d-csdm-profile-wa` clones (2024) were not used.

## 3. Method

The JSON-LD bindings were taken as the reference, because they connect the schema to the definitions.

1. **Bound IRIs.** Every term definition in the built (merged, annotated) `context.jsonld` files of `3d-csdm-common`,
   the WA profile (which pulls in ICSM) and Land Parcels, expanded to absolute IRIs.
2. **Used IRIs.** Every predicate and `rdf:type` value in the uplifted Turtle for all examples and tests in
   `3d-csdm-common/build/tests` and `3d-csdm-profile-wa/build/tests` (34 WA files, plus the common ones).
3. **Declared IRIs.** Every typed subject in the ontologies of this repo, Land Parcels (`parcels.ttl`,
   `spatialRepresentationDefinition`, `parcelSpatialRepresentationDefinition`) and the compoundName ontology.
4. The three sets were compared, and the definitions of bound terms were checked against the schema (the JSON
   types and where the property appears).
5. The WA profile documentation was read for model changes that are documented but not yet in the schema
   (built strata, 2.5D/liminal, vocabulary decisions).

## 4. Summary of findings

| Area | Finding |
|---|---|
| `container` | 7 bound properties not declared; `parcels` still points at the retired CSDM parcels namespace; a wrongly labelled `surveyobs:Measure` class; design-process meta-classes mixed into the model |
| `surveyfeatures` | 8 bound terms not declared (including `SurveyedVector`, `fromSurvey`, `geodeticid`, sensor properties); `distance` is defined as an object property but always carries a number; `state` has the wrong domain |
| `surveyobs` | the 4 bound accuracy properties are not declared; the 4 declared quality properties are not bound to anything; sensor and GeoPose terms are not declared anywhere |
| `geometry` / `geosparql3d` | none of the terms are bound; the module predates Topo-Feature and overlaps it; it declares terms inside the GeoSPARQL and SKOS namespaces |
| `parcels` (working) | superseded by Land Parcels (`https://w3id.org/ogc/ladm/parcels/`): no context binds the CSDM parcels IRIs |
| Land Parcels | 19 bound `ladm/parcels/` terms are not declared in its ontology; the spatial-representation ontologies are complete against their bindings |
| Topo-Feature | **no ontology at all**: 17 `topo:` terms and 10 terms placed in the `geojson:` namespace are bound but not defined; several context defects |
| Common Patterns | `com:qualityClass`, `com:qualityMeasure`, `com:Measure`, `com:value`, `com:RelevantJurisdictionalCodelist` and `com:Common` are used and bound, but the published utility ontology declares only the compoundName terms |
| SOSA | consistent; no change needed |

## 5. Proposed changes to the ontologies in this repository

Notation: `container:` = `https://linked.data.gov.au/def/csdm/container/`, `surv:` = `.../csdm/surveyfeatures/`,
`surveyobs:` = `.../csdm/surveyobs/`, `ladm:` = `https://w3id.org/ogc/ladm/parcels/`,
`com:` = `https://w3id.org/ogc/utils/label/`, `topo:` = `https://purl.org/geojson/topo#`.

Where a term's IRI is in one module's namespace but logically belongs to another module (this already happens
for `surv:age`, `surv:Traverse` and `surv:horizontalDistance`, which are declared in `surveyobs.ttl`), the IRI is kept
and the declaration goes in the module where the concept belongs, with `rdfs:isDefinedBy` pointing to that module.

### 5.1 `model.container` (`container.ttl`)

**Add** (all bound in the `CSD` context; all except `surveyDescriptors` occur in the uplifted examples):

| Term | Kind | Range / notes | JSON property |
|---|---|---|---|
| `container:surveyType` | ObjectProperty | `skos:Concept`. Today it is declared only in `container.shapes.ttl` as an `rdf:Property`; move the declaration into the ontology | `surveyType` |
| `container:surveyDescription` | DatatypeProperty | `xsd:string` | `surveyDescription` |
| `container:surveyDescriptors` | ObjectProperty | `com:CompoundName` | `surveyDescriptors` |
| `container:annotations` | ObjectProperty | annotation set: `prof:hasRole` (role) and `dct:description` | `annotations` |
| `container:supportingDocuments` | ObjectProperty | links with a role (JSON-FG link-role pattern) | `supportingDocuments` |
| `container:observedVectors` | ObjectProperty | feature collection of `surv:ObservedVector` | `observedVectors` |
| `container:adoptedVectors` | ObjectProperty | feature collection of `surv:AdoptedVector` | `adoptedVectors` |

**Change:**

- `container:vectorObservations`: set `rdfs:range surveyobs:VectorObservations`, and
  `container:occupationObservations`: set `rdfs:range surveyobs:OccupationObservations` (both currently
  `sosa:ObservationCollection`). The data only types these collections as `sosa:ObservationCollection`, so the
  narrower ranges let RDFS inference give them their CSDM types. Both are subclasses of `sosa:ObservationCollection`,
  so nothing that holds today stops holding.
- `container:referencedCSD`: add `rdfs:range container:CSD`.
- `container:parcels`: keep the range `geometry:FeatureCollection`, and add a comment that the members are
  `ladm:Parcel`.
- Replace `parcel:ParcelModel rdfs:subClassOf container:ClassIn3DCadastre` (retired CSDM parcels namespace) with the
  equivalent for `ladm:Parcel`, or drop it (see 5.8).
- Make the definitions of `container:purpose`, `horizontalCRS`, `compoundCRS`, `verticalDatum` and `adminUnit`
  consistent: object properties whose range is `skos:Concept` or a CRS IRI (all are bound with `@type: @id`).

**Remove or move:**

- `surveyobs:Measure` (declared here with the label "GeoSPARQL 1.2 (3D profile)", which is a copy-paste error).
  `com:Measure` covers it. Delete it, or declare it as `owl:equivalentClass com:Measure` with `owl:deprecated true`.
  No context binds it.
- Move the design meta-classes `container:ModelledElement`, `ClassIn3DCadastre`, `StandardClass` and `GeoSPARQL-3D`
  (and the `rdfs:subClassOf` axioms that attach model classes to them) to a utility block, for example
  `utility.ontexamples` or a new `utility.modelindex`. They classify model elements for documentation and are not part
  of the domain model. No context binds them. **Decision D1.**

**Orphan term:** the `CSD` context binds `locality` to `https://linked.data.gov.au/def/csdm/csd/locality`, a namespace
no module owns. The CSD schema has no `locality` property; addresses use `sdo:addressLocality` through the ICSM
address context. **Decision D2:** declare it in `container` as `rdfs:subPropertyOf schema:addressLocality`, or ask
for the binding to be removed from the common context.

### 5.2 `model.surveyfeatures` (`surveyfeats.ttl`)

**Add:**

| Term | Kind | Definition basis | Bound by |
|---|---|---|---|
| `surv:SurveyedVector` | Class | `rdfs:subClassOf surv:SurveyedLine`; superclass of `ObservedVector` and `AdoptedVector`. This is the schema's abstract `SurveyedVector` (`distance`, `vectorPurpose`, `comment`) | common `SurveyFeatures` context (see D3) |
| `surv:SubtendedAngle` | Class | a topology whose three references define an angle at a vertex (`SubtendedAngleVector` in the CSD schema) | not yet bound in common (see §8) |
| `surv:fromSurvey` | ObjectProperty | domain `surv:AdoptedVector`; the survey (CSD or plan) the vector was adopted from | `fromSurvey` |
| `surv:geodeticid` | ObjectProperty | domain `surv:GeodeticReferenceMark`, range `com:CompoundName`, `rdfs:subPropertyOf com:name` | `geodeticid` |

**Change (definitions that conflict with how the schema uses the term):**

- `surv:distance`: change from `owl:ObjectProperty` (range `surv:Distance`, domain `surv:SurveyedLine`) to
  `owl:DatatypeProperty` with range `xsd:double` and no domain. All 321 uses in the uplifted examples are numeric
  literals, on vector features and on `sosa:hasResult` nodes. Keep `surv:Distance` as the measure class, with a note
  that the exchange encoding uses a plain number. The same applies to `surv:horizontalAngle` and
  `surv:verticalAngle`, which are not bound at present.
- `surv:state`: change the domain from `surv:SurveyMark` to `surv:Monument`. In the schema, `state` is a property of
  the `monumentedBy` object, together with `condition`, `form` and `replaces`.
- `surv:monumentedBy`: add domain `surv:SurveyMark` and range `surv:Monument` (both are missing today).
- `surv:purpose`, `surv:vectorPurpose`, `surv:condition`, `surv:form`: add range `skos:Concept` (bound with
  `@type: @id` to jurisdictional vocabularies). Keep the existing codelist classes (`SurveyPointPurpose`,
  `MonumentCondition` and so on) and link them with `skos:scopeNote` or `rdfs:seeAlso`. `condition` and `form`
  currently have the codelist classes as their range, but the data never types the concepts with them.
- `surv:age` (declared in `surveyobs.ttl`): make it an `owl:DatatypeProperty` with range `xsd:string`, domain
  `surv:OccupationMark`, and the schema's description ("may be constrained to a number or range using a regex").

**Decision D3:** the common `SurveyFeatures` context binds the JSON `featureType` value `AdoptedVector` to
`surv:SurveyedVector`, not to the declared class `surv:AdoptedVector`. Declaring `surv:SurveyedVector` keeps the
current output valid either way. The context mapping looks like an error, and correcting it (to `surv:AdoptedVector`)
would change the uplift output, so it needs agreement before the common context changes.

### 5.3 `model.surveyobs` (`surveyobs.ttl`)

**Add, as the terms the `quality` datatype binds** (they apply to the `sosa:hasResultQuality` node):

| Term | Kind | Notes |
|---|---|---|
| `surveyobs:angleAccuracyMeasure` | DatatypeProperty | `xsd:double`, `rdfs:subPropertyOf com:qualityMeasure` |
| `surveyobs:distanceAccuracyMeasure` | DatatypeProperty | `xsd:double`, `rdfs:subPropertyOf com:qualityMeasure` |
| `surveyobs:angleAccuracyClass` | ObjectProperty | `skos:Concept`, `rdfs:subPropertyOf com:qualityClass` |
| `surveyobs:distanceAccuracyClass` | ObjectProperty | `skos:Concept`, `rdfs:subPropertyOf com:qualityClass` |

**Deprecate** (`owl:deprecated true`, `dct:isReplacedBy` the matching new term). These are not bound anywhere:
`surveyobs:angleQuality`, `angleQualityMeasure`, `distanceQuality`, `distanceQualityMeasure`. As a side effect this
removes an existing inconsistency: `distanceQuality` is an object property declared as a sub-property of the
datatype-valued `com:qualityMeasure`.

**Change:** `surveyobs:angleType` and `surveyobs:distanceType`: add range `skos:Concept`.

**Add the observation-result and equipment terms**, keeping their bound IRIs:

| Term | Kind | Notes |
|---|---|---|
| `surv:pose` | ObjectProperty | on a `sosa:Result`; range a GeoPose (see 6.3) |
| `surv:sensorType` | ObjectProperty | `skos:Concept` (equipment-type vocabularies); bound by the ICSM profile |
| `surv:sensorRole` | ObjectProperty | `skos:Concept`; bound by the ICSM profile |
| `surv:lastCalibrated` | DatatypeProperty | date or dateTime; bound by the ICSM profile |
| `https://linked.data.gov.au/def/csdm/sensors/DifferentialGPS` | Class | `rdfs:subClassOf sosa:Sensor`; the schema `const` for `sensorType` |
| `.../csdm/sensors/baseSensor`, `.../csdm/sensors/roverSensor` | Property | the component receivers of a differential GNSS system. The JSON value is a string, so these produce literals |

**Decision D4 (sensors):** `baseSensor` and `roverSensor` describe what `sosa:hasSubSystem` describes, and that
property already appears in the ICSM and WA examples. They can only be declared `rdfs:subPropertyOf
sosa:hasSubSystem` if the values become IRIs (`@type: @id` in the context). Otherwise declare them as plain
datatype properties and record the overlap. Also note the conflict between the common context's property-scoped
`"sensorType": "@type"` (under `madeBySensor`) and the ICSM top-level `"sensorType": "surv:sensorType"`. In the
uplifted examples the scoped `@type` form wins (for example `rdf:type icsm-equipment-type:ts`), so
`surv:sensorType` only appears outside `madeBySensor`.

**Unbound property:** the schema `SurveyVectorObsResult.angle` (a number) has no binding and is dropped on uplift.
See §8.

### 5.4 `model.surveyprov` (`surveyprov.ttl`)

- Move `survprov:SurveyType` (a codelist class currently declared in `container.shapes.ttl`) into this ontology as
  `rdfs:subClassOf com:RelevantJurisdictionalCodelist`, the same pattern as `SurveyActivityType`.
- No new bound terms. Provenance in the exchange model comes from the `bblock-prov-schema` building block (PROV-O
  terms; WA uses `activityType` as `@type`), which fits `SurveyActivity`, `SurveyAgent` and `SurveyEntity` as they
  are.

### 5.5 `model.geometry` and `model.geosparql3d`: refactoring

None of the terms in these modules are bound by any context. The exchange model now encodes geometry and topology
with Topo-Feature (`topo:Edge`, `Face`, `Ring`, `Shell`, `Solid`, `AggregateSolid`, `directedReferences`,
`orientation`) and the Land Parcels spatial-representation ontology (vertical extents and boundary definitions).
Proposal:

1. **Align with Topo-Feature** once the topo ontology exists (6.1):
   `geometry:BoundaryFace` → `topo:Face`, `BoundaryEdge` → `topo:Edge`, `BoundaryNode` → point features,
   `geometry:hasTopology` → `geojson:topology`, `geometry:nodeFrom`/`nodeTo`/`directedNode` → `topo:directedReferences`
   with `topo:orientation`, `geometry:solidMember` → `topo:shells`/`topo:Solid`. Use `rdfs:subClassOf` where the
   CSDM class adds boundary meaning, and `skos:closeMatch` otherwise.
2. **Align the extrusion terms with spatial-representation:** `geometry:ExtrudedGeometry`, `ExtrudedSurface`,
   `ExtensionRule` and `extension` overlap `spatial-representation:VerticalExtent`, `VerticalBoundaryDefinition` and
   `ladm:zmin`/`zmax`. Add `skos:closeMatch` mappings and mark the CSDM terms deprecated where they are fully
   replaced. **Decision D5.**
3. **Stop declaring terms in namespaces CSDM does not own:** `geo:touchesInward`, `geo:touchesOutward`,
   `geo:extension`, `geo:isOutward`, `geo:asGMLTopo` and `skos:extrusion` are declared in the GeoSPARQL and SKOS
   namespaces. Re-declare them in `geometry:`. They are unbound, so no link breaks. Anything that is still
   needed can be proposed to GeoSPARQL 1.3.
4. **Retire `geosparql3d`:** it holds 5 triples, a TODO, and an `owl:imports` of
   `https://linked.data.gov.au/def/csdm/geometryprim`, which does not resolve. Fold its profile statement into
   `geometry` or `all`, and update `model.all`'s `dependsOn`.

### 5.6 `model.all` (`csdm.ttl`, the PROF profile)

Update the `prof:hasResource` descriptors to list the modules the model is now built from: Land Parcels ontology
and spatial-representation (`@ogc/land-parcels`), the Topo-Feature ontology (6.1), Common Patterns (6.2), GeoPose
(6.3) and SOSA. Remove the reference to the CSDM parcels module, and the `geosparql3d` reference if 5.5.4 is accepted.

### 5.7 SHACL shapes in this repository

- Add shapes for the new properties only where the schema has a rule (for example the `surv:fromSurvey` cardinality
  on adopted vectors). Otherwise leave the shapes alone.
- `vector_observations.shapes.ttl`: the unused property shape `:FeatureIsASurveyVector` (already reported in the
  README) should either be attached to a node shape or removed.

### 5.8 `working/parcels`: retire in favour of Land Parcels

No context binds any `https://linked.data.gov.au/def/csdm/parcels/` IRI. The common and WA schemas bind the
`ladm:` terms. Proposal:

- Do not build the CSDM parcels ontology as a model block.
- Replace it with a small alignment block, **`icsm.csdm.model.parcels-alignment`**, that maps each CSDM parcels term
  to its `ladm:` counterpart (`owl:equivalentClass` / `owl:equivalentProperty`, `dct:isReplacedBy`), using the
  existing `working/parcels/reconciliation/differences.csv`. This keeps the older IRIs, which appear in published
  documentation, resolvable.
- CSDM-only parcel terms with no `ladm:` counterpart (`parcels:ParcelModel`, `parcels:area` as distinct from
  `surfaceArea`) should be raised for addition to Land Parcels or explicitly dropped. **Decision D6.**

## 6. New ontology building blocks needed

### 6.1 Topo-Feature ontology: **required** (topo-feature repo, e.g. `ogc.geo.topo.ontology`)

Topo-Feature has contexts but no ontology. The CSDM's whole geometry and topology meaning depends on it.

**Declare in the `topo:` namespace** (all bound; most are used in the WA examples):

- Classes: `topo:Edge`, `Face`, `Ring`, `Shell`, `Solid`, `AggregateSolid`.
- Properties: `topo:relatedFeatures`, `directedReferences`, `ref`, `orientation`, `points`, `edges`, `rings`, `faces`,
  `shells`, `solids`, `circumference`.

**Terms Topo-Feature binds into the GeoJSON-LD namespace** (`https://purl.org/geojson/vocab#`): `topology`, `Arc`,
`ArcWithCenter`, `ArcByChord`, `CircleByCenter`, `CubicSpline`, `radius`, `arcLength`, `startTangentVector`,
`endTangentVector`. The published GeoJSON-LD vocabulary does not define them. They are used in the examples
(`geojson:topology` 1,206 times), so the IRIs must stay. Declare them in the topo ontology with
`rdfs:isDefinedBy` the topo ontology, and note that they are extensions to that namespace. **Decision D7:** whether
to also mint `topo:` equivalents for future use.

**Context defects in topo-feature to fix at the same time** (these changes leave existing uplift output the same):

| File | Defect |
|---|---|
| `datatypes/topology/context.jsonld` | `"ref": {"@id": "topo:ref", "type": "@id"}`: `type` should be `@type` |
| `features/topo-face`, `features/topo-shell` contexts | `"ref": {"@id": "@id"}` contradicts the `topo:ref` binding in `topology` |
| `features/topo-ring/context.jsonld` | uses the `topo:` prefix without declaring it (works only through inheritance) |
| `features/topo-feature-collection/context.jsonld` | has no `@context` wrapper (`{"properties": "@nest"}`) |
| `features/topo-arc`, `topo-line` contexts | empty objects with no `@context` key |

**Decision D8:** `references` (an ordered member list) and `relationships` (link objects with `rel`, `role`, `href`)
both map to `topo:relatedFeatures`. They mean different things. Separating them (for example a new
`topo:relationships` property) would change uplift output for every consumer of `topo:relatedFeatures`, so it needs
agreement first. The ontology can define `topo:relatedFeatures` broadly enough to cover both in the meantime.

### 6.2 Common Patterns ontology: **required** (bblocks-utility)

The model ontologies, the CSDM shapes and the compoundName `shapes.shacl` all use `com:Measure`, `com:value`,
`com:qualityMeasure`, `com:qualityClass`, `com:RelevantJurisdictionalCodelist` and `com:Common`. The common contexts
bind `ptQuality` → `com:qualityClass` and `ptQualityMeasure` → `com:qualityMeasure` (459 uses in the examples).
The utility register's ontology only declares `CompoundName`, `NamePart`, `name`, `namePartRef` and `namePartType`.
This repository's README refers to `ogc.bbr.utils.commonpatterns`, but that block does not exist on utility `master`
(the `commonpatterns-ontology` branch has the same compoundName-only sources).

Proposal: complete the Common Patterns ontology in bblocks-utility, either as its own block
`ogc.bbr.utils.commonpatterns` or by adding the six terms to the compoundName ontology, which already uses the same
namespace and shapes. Then change the model blocks' `dependsOn` from `ogc.bbr.utils.compoundName.ontology` to that
block if it is a separate one. **Decision D9.**

### 6.3 GeoPose ontology: **new** (small)

The `SurveyObservations` context binds observation poses to `https://linked.data.gov.au/def/csdm/utils/geopose/`
(`position`, `angles`, `h`, `yaw`, `pitch`, `roll`; `lat` and `lon` use W3C WGS84 `geo:`). Nothing declares this
namespace. OGC GeoPose 1.0 defines a JSON encoding but no RDF vocabulary. Proposal: a small ontology block that
declares these 6 terms with definitions taken from GeoPose 1.0 Basic-YPR. **Decision D10:** host it here
(`icsm.csdm.model.geopose`), or upstream in bblocks-utility since the IRI path is already `/utils/`.

### 6.4 Parcels alignment block: **new** (this repo)

See 5.8.

### 6.5 Anticipated, not yet needed: built-strata and 2.5D/liminal terms

The WA proposals (`proposals/development/built-strata/*`, `2-5d-liminal/*`) describe new properties: `componentRole`,
`boundaryRole`, `boundaryFaceRef`, `referenceFeatureRef`, `boundaryCoverage.fullBoundaryCoverage`, `entitlementTotal`,
`schemeName`, `schemeNumber`, `schemeRef`. They also describe vocabularies (`component-role`, `boundary-role`,
`boundary-reference`, `occupation-feature`, `source-scope`, `reference-kind`, `derivation-mechanism`, and others).
**None of these is in any schema or context yet**; the scope note calls them "a proposal, not an approved bblock".
Nothing should be added to the ontology until a `wa-built-strata` (or common) schema binds them. When that happens:

- the boundary-definition properties belong in the Land Parcels `spatial-representation` ontology, which already
  holds `VerticalBoundaryDefinition`, `limitRole`, `sourceReference` and the related terms;
- `entitlementTotal` belongs in `ladm:`, next to `entitlementPortion` (WA decision D7 makes both parcel properties).

The WA scope note also raises `ParcelAggregate` as a typed feature (question 3). `ladm:ParcelAggregate` already exists
in the Land Parcels ontology, so binding it as a `featureType` value needs no ontology change.

## 7. Changes needed in component ontologies outside this repository

### 7.1 Land Parcels (`bblocks-land-parcels/_sources/ontology/parcels.ttl`)

Declare the 19 `ladm:` terms that the `parcel` context binds but the ontology does not define:

| Group | Terms |
|---|---|
| Interests | `interestLink`, `interestName`, `interestType`, `interestDescription`, `interestDateInForce`, `interestDateExpires`, `statuteLink`, `statuteName`, `benefitedPartyLink`, `benefitedPartyName`, `referencedParcel`, `originalSurveyLink`, `burdened`, `benefited`, `entitlementPortion`, `liabilityPortion` |
| Parcel | `floor`, `parcels`, `bearingRotation` |

`ladm:bearingRotation` duplicates `container:bearingRotation`. Declare one as `rdfs:subPropertyOf` the other, or
both as `owl:equivalentProperty`. **Decision D11.**

The `spatial-representation` and `parcel-vertical-boundary` ontologies (both in CSDM namespaces under
`https://linked.data.gov.au/def/csdm/`) define all 39 of the IRIs bound to them. They need no change.
**Decision D12 (governance):** these are CSDM-namespaced ontologies hosted in an OGC incubator repository. Moving
them here would create a circular dependency, because the Land Parcels schema binds them. The recommendation is to
keep them where they are, list them in `model.all` (5.6), and record the ownership arrangement.

### 7.2 Topo-Feature

See 6.1.

### 7.3 SOSA (ogcapi-sosa)

No changes. The CSDM uses `sosa:hasMember`, `hasResult`, `hasFeatureOfInterest`, `observedProperty`, `madeBySensor`,
`usedProcedure`, `resultTime`, `hasSubSystem` and `hasResultQuality` as SOSA defines them (`hasResultQuality` is in
the revised SOSA core, `sosa-observation.ttl`). Check that the cross-domain-model `sosa` block that the model blocks
depend on is the revised SOSA that includes `hasResultQuality`.

### 7.4 Common Patterns (bblocks-utility)

See 6.2.

## 8. JSON-LD context issues found (for the schema repositories; not ontology changes)

These are outside this repository. They are listed because they decide which ontology terms get used. All of them
add bindings; none changes an existing binding, except where marked as a decision.

| Repo / context | Issue | Effect today |
|---|---|---|
| common `SurveyFeatures` | `featureType` values `OccupationMark`, `SurveyMark`, `SurveyPoint`, `SurveyedVector` are not bound | uplifts to example-base IRIs such as `.../csd-example/OccupationMark` |
| common `CSD` | topology type `SubtendedAngle` (and WA's `AggregatePolygon`) not bound | 622 `rdf:type` values like `https://www.wa-example.com/features/SubtendedAngle` |
| common `SurveyObservations` | `hasResult.angle` not bound | angle values dropped on uplift |
| common `CSD` | `adoptedObservations` (in the schema) not bound | dropped on uplift |
| common `SurveyFeatures` | `AdoptedVector` → `surv:SurveyedVector` | see D3 |
| common `CSD` | `locality` → orphan `csd:locality` | see D2 |
| common `SurveyObservations` / ICSM `common` | two different bindings for `sensorType` | see D4 |
| ICSM `datatypes/address` | prefix declared as `ads` but used as `ad:` (`"ad:propertyNumber"` and so on); declared IRI `https:/icsm.org.au/...` has one slash | uplift produces relative IRIs `ad:propertyNumber`, `ad:streetName`, `ad:streetType` |
| common `_sources/csdm/shapes/*` | stale copies of this repo's shapes, still using the old `.../csdm/commonpatterns/` namespace; `parcel_module.shapes.ttl` targets `.../csdm/parcels/` classes | the CSD parcel shapes never match the `ladm:` data, so they validate nothing |

**Refactoring recommendation:** `3d-csdm-common` should depend on this repository's shapes (through `dependsOn` on
the `icsm.csdm.model.*` blocks) instead of carrying copies. That removes the drift shown in the last row.

## 9. Link-preservation rules applied

1. No IRI that any context binds is renamed or removed. Every proposed change to a bound term only adds or
   corrects its definition (type, domain, range, labels, definition text).
2. Terms are deprecated (`owl:deprecated`, `dct:isReplacedBy`) or moved only when no context binds them
   (`surveyobs:*Quality*`, the geometry namespace-squatting terms, `surveyobs:Measure`, the container meta-classes).
3. Superseded vocabularies (CSDM parcels, geometry extrusion) are kept resolvable through equivalence or
   close-match mappings, not deleted.
4. Changes that would alter uplift output (D3, D8, and making `baseSensor`/`roverSensor` IRI-valued under D4) are
   left as decisions and not assumed.

## 10. Decisions requested

| ID | Decision | Recommendation |
|---|---|---|
| D1 | Move container meta-classes (`ModelledElement` and so on) to a utility block | Yes |
| D2 | `csd:locality`: declare, or remove from the context | Declare as a sub-property of `schema:addressLocality` and ask for the binding to be removed |
| D3 | Correct `AdoptedVector` → `surv:AdoptedVector` in the common context | Yes, after the ontology declares both classes |
| D4 | `baseSensor`/`roverSensor` as IRI-valued sub-properties of `sosa:hasSubSystem`; settle the `sensorType` dual binding | Yes to both; keep the scoped `@type` form |
| D5 | Deprecate the geometry extrusion terms in favour of spatial-representation | Deprecate where the replacement is complete; otherwise `closeMatch` |
| D6 | CSDM-only parcel terms: propose to Land Parcels, or drop | Propose `area` vs `surfaceArea` and `ParcelModel` upstream |
| D7 | Mint `topo:` equivalents for the terms in the `geojson:` namespace | Not now; declare them where they are |
| D8 | Separate `relationships` from `references` in Topo-Feature | Defer; it changes uplift output |
| D9 | Common Patterns as a separate block or merged into compoundName | Separate `ogc.bbr.utils.commonpatterns`, as the README already describes |
| D10 | Where the GeoPose ontology lives | bblocks-utility (the IRI is already under `/utils/`) |
| D11 | `ladm:bearingRotation` vs `container:bearingRotation` | `container:` as a sub-property of `ladm:` |
| D12 | Ownership of the CSDM-namespaced spatial-representation ontologies in Land Parcels | Keep them there; record it |

## 11. Implementation plan (after review)

1. **This repo:** edit `container.ttl`, `surveyfeats.ttl`, `surveyobs.ttl`, `surveyprov.ttl`, `geometryprim.ttl`
   and `csdm.ttl` as in §5. Add the `parcels-alignment` block and, depending on D10, the `geopose` block. Update
   the `bblock.json` `dependsOn` lists and the README.
2. **topo-feature:** add the ontology block (6.1) and fix the contexts.
3. **bblocks-utility:** complete Common Patterns (6.2), and GeoPose if D10 places it there.
4. **bblocks-land-parcels:** add the 19 terms (7.1).
5. **Verification:** re-run the comparison in §3 (the scripts can be added to `tools/`). The target is zero bound
   IRIs in the CSDM, `ladm:`, `topo:` and `com:` namespaces without a declaration. Then rebuild this register and
   `3d-csdm-common`, and confirm that the uplifted Turtle for all examples is unchanged and that SHACL validation
   still passes.

## 12. Implementation status (2026-10-30)

Implemented, uncommitted, in the working trees of the repositories named:

| Item | What was done | Repository |
|---|---|---|
| 6.2 Common Patterns (D9) | New block `icsm.csdm.model.commonpatterns` (`_sources/model/commonpatterns/`; first created in 3d-csdm-common, then moved here to keep ontologies separate from schemas): `Common`, `Measure`, `value`, `qualityMeasure`, `qualityClass`, `RelevantJurisdictionalCodelist`, `Report` in the original `https://linked.data.gov.au/def/csdm/commonpatterns/` namespace, plus deprecated equivalents of the old `CompoundName`, `NamePart`, `name` IRIs. SHACL shapes, an example and two fail tests. | 3d-csdm-model |
| Cleanup | The stray `_sources/rdfs/commonpatterns.ttl` (different namespace, unreferenced) was removed. | 3d-csdm-common |
| JSON-LD | `SurveyFeatures` context: `ptQuality` and `ptQualityMeasure` now bind to `commonpatterns:qualityClass` / `qualityMeasure` in the CSDM namespace (**changes uplift output**); `name` stays `https://w3id.org/ogc/utils/label/name`. `SurveyFeatures` now depends on `icsm.csdm.model.commonpatterns` and `ogc.bbr.utils.compoundName.ontology`; the common register imports the model register (`https://surroundaustralia.github.io/3d-csdm-model`). | 3d-csdm-common |
| References | Compound-name terms use `ogc.bbr.utils.compoundName.ontology`; `Measure`, `qualityMeasure`, `RelevantJurisdictionalCodelist` use the new block, in the model ontologies, shapes, evidence closure and `working/parcels`. Model blocks depend on the new block; the register imports topo-feature. pyLODE config updated. | 3d-csdm-model |
| References | `parcels.ttl` codelist classes subclass `commonpatterns:RelevantJurisdictionalCodelist`; `topoobjects.ttl` closure updated to the new `qualityMeasure` IRI. | bblocks-land-parcels |
| References | `profiles/wa-pointnames-shacl.ttl` targets `https://w3id.org/ogc/utils/label/name` (it previously targeted the old CSDM IRI and matched nothing). | 3d-csdm-profile-wa |
| 6.1 Topo-Feature ontology (D7: terms declared where they are) | New block `ogc.geo.topo.ontology` (`_sources/ontology/`): 8 classes and 11 properties in `topo:`, and the 10 extension terms in the `geojson:` namespace. SHACL shapes, an example and two fail tests. The 7 schema blocks whose contexts bind these terms now depend on it. Context defects (§6.1 table) not yet fixed. | topo-feature |
| D1 | Meta-classes and their classification axioms moved to new block `icsm.csdm.utility.modelindex`; `surveyobs:Measure` is now a deprecated equivalent of `commonpatterns:Measure`. | 3d-csdm-model |
| 5.5 / D5 | Geometry: six terms moved from `geo:`/`skos:` to `geometry:` (ontology, shapes, examples); `skos:closeMatch`/`relatedMatch` mappings to Topo-Feature and spatial-representation (no deprecations: no term is fully replaced); `geosparql3d` retired (moved to `working/retired/geosparql3d/`). | 3d-csdm-model |

Verification: local builds of topo-feature, 3d-csdm-model (against a local export of topo-feature) and 3d-csdm-common
(against a local export of the model register). The new blocks pass, and their fail tests fail as intended. topo-feature reports 3 failing schema blocks
(topo-face, topo-shell, topo-feature-multi-collection), all from topo-validator plugin geometry checks; an unmodified
build of HEAD fails in exactly the same way.

Not yet done: the shapes issue (§8, last row), context fixes in §8, and items 5.1 to 5.4, 5.6, 5.8 and 7.1.
