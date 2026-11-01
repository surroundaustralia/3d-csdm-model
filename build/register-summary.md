# 3D Cadastral Survey Data Model (CSDM) Ontologies

The ontology modules of the ICSM 3D Cadastral Survey Data Model (3D CSDM), packaged as OGC Blocks.
The CSDM model (`icsm.csdm.model.*`) - one block per ontology module, with its SHACL shapes and canonical
examples - is kept separate from the utility blocks (`icsm.csdm.utility.*`) that support the design process
and documentation: implementation evidence, requirements meta-model, attributions and documentation configuration.


Source: the `csdm_model` directory of [icsm-au/3d-csdm](https://github.com/icsm-au/3d-csdm/tree/main/csdm_model).

Dependencies are declared to the common ontologies registered in the
[Cross-domain model](https://ogcincubator.github.io/cross-domain-model/) (GeoSPARQL, SOSA, PROV, PROF,
Dublin Core Terms, schema.org) and the [SKOS](https://ogcincubator.github.io/bblocks-skos/) building blocks.
Compound names are reused from the [Utility](https://ogcincubator.github.io/bblocks-utility/) register
(`ogc.bbr.utils.compoundName.ontology`). The CSDM Common Patterns (measures, quality classes and measures,
jurisdictional codelists, reports) are the `icsm.csdm.model.commonpatterns` block of this register.
Geometry topology is aligned with the [Topo-Feature](https://ogcincubator.github.io/topo-feature/) ontology
(`ogc.geo.topo.ontology`).

The Cadastral Parcels module depends on the [Land Parcels](https://ogcincubator.github.io/bblocks-land-parcels/)
ontology, which was derived from it. A concept-level comparison (ignoring IRIs) is provided in the
parcels block to support reconciliation of the two.

The [schema building blocks](https://icsm-au.github.io/3d-csdm-schema/) for the CSDM exchange format are
maintained separately.


## Building Blocks

### `icsm.csdm.model.geopose` — CSDM GeoPose

**Type:** model

RDF terms for the GeoPose Basic-YPR structure (position and yaw, pitch, roll angles) used by 3D CSDM survey observation results.

### `icsm.csdm.utility.ontexamples` — Ontology Example Shapes

**Type:** model

Edited version of PROF shapes for creating and attaching example resources to ontology classes.

### `icsm.csdm.utility.reqmetamodel` — Requirements Meta-model

**Type:** model

Shapes-based meta-model linking model elements to canonical examples and requirements (used by the CSDM examples).

### `icsm.csdm.model.geometry` — CSDM Geometry Primitives

**Type:** model

Extends GeoSPARQL with a named subset of ISO 19107 concepts for 3D solids and 3D topology amongst features. A candidate extension for GeoSPARQL 1.1. Includes the former GeoSPARQL 3D profile placeholder module, and maps its terms to the Topo-Feature and spatial-representation ontologies used by the exchange encoding.

### `icsm.csdm.model.commonpatterns` — CSDM Common Patterns

**Type:** model

Common implementation patterns not directly supported by other standards: qualified measures, quality classes and measures, jurisdictional codelists and reports. Compound names are reused from the OGC Utility compoundName ontology.

### `icsm.csdm.utility.attributions` — CSDM Attributions

**Type:** model

Persons, organisations and groups referenced for attribution of the CSDM.

### `icsm.csdm.model.parcelsalignment` — CSDM Cadastral Parcels Alignment

**Type:** model

Deprecates the terms of the retired CSDM Cadastral Parcels module and maps each to the OGC Land Parcels term that replaces it, so the CSDM parcels IRIs still resolve.

### `icsm.csdm.model.surveyfeatures` — CSDM Survey Features

**Type:** model

Feature types defined by cadastral surveys (survey marks, boundaries, monuments etc.).

### `icsm.csdm.utility.impspecs` — CSDM Implementation Specifications

**Type:** model

SKOS taxonomy of conformance types (specifications) used to classify implementation examples.

### `icsm.csdm.model.surveyobs` — CSDM Survey Observations

**Type:** model

Survey observations modelling for cadastral surveys, as a specialisation of SOSA.

### `icsm.csdm.model.surveyprov` — CSDM Survey Provenance

**Type:** model

Survey provenance modelling for cadastral surveys - a profile of PROV-O.

### `icsm.csdm.model.container` — CSDM Survey Plan Container

**Type:** model

Import closure for the 3D model packages and aggregation containers for exchange objects.

### `icsm.csdm.model.all` — 3D Cadastral Survey Data Model (complete)

**Type:** model

ICSM Conceptual Model for 3D Cadastral Survey Dataset Submissions. A PROF profile aggregating all CSDM model modules.

### `icsm.csdm.utility.evidence` — CSDM Design Evidence

**Type:** model

Canonical example closure, implementation examples from existing exchange formats (LandXML, ePlan, InfraGML, IFC, LADM etc.) and competency queries used in the design of the CSDM.

### `icsm.csdm.utility.modelindex` — CSDM Model Index

**Type:** model

Classification of 3D CSDM model elements (modelled element, class defined in the 3D cadastre model, key class, GeoSPARQL 3D profile class) used to organise the model documentation. Moved from the container module; not part of the domain model.

### `icsm.csdm.utility.documentation` — CSDM Documentation Configuration

**Type:** model

pyLODE configuration describing the CSDM modules, their shapes and supporting resources for generating the model documentation.

