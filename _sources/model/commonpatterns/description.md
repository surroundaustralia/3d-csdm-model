## CSDM Common Patterns

Implementation patterns used across the 3D Cadastral Survey Data Model that are not directly supported by other
standards:

- `Measure`, `value`, `qualityMeasure`: a measured value qualified by a numeric quality measure;
- `qualityClass`: a reference to a quality or accuracy class concept;
- `RelevantJurisdictionalCodelist`: the superclass of the codelists each jurisdiction defines;
- `Report`: a typed report described with the Profiles vocabulary resource descriptor pattern.

The namespace is `https://linked.data.gov.au/def/csdm/commonpatterns/`, the namespace of the original CSDM Common
Patterns module.

Compound names (`CompoundName`, `NamePart`, `name`, `namePartType`, `namePartRef`) are defined by the OGC Utility
[compoundName ontology](https://ogcincubator.github.io/bblocks-utility/bblock/ogc.bbr.utils.compoundName.ontology)
in `https://w3id.org/ogc/utils/label/`. The original Common Patterns IRIs for `CompoundName`, `NamePart` and `name`
are kept here as deprecated equivalents of those terms.

The Survey Features schema binds `ptQuality` to `qualityClass` and `ptQualityMeasure` to `qualityMeasure`.
