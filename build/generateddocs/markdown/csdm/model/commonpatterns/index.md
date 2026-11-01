
# CSDM Common Patterns (Model)

`icsm.csdm.model.commonpatterns` *v0.2*

Common implementation patterns not directly supported by other standards: qualified measures, quality classes and measures, jurisdictional codelists and reports. Compound names are reused from the OGC Utility compoundName ontology.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

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

## Examples

### Quality class, quality measure and qualified measurement
A survey point carrying a quality class and a numeric quality measure (the RDF form of the `ptQuality` and
`ptQualityMeasure` properties of the Survey Features schema), and a qualified measurement.
#### turtle
```turtle
@prefix commonpatterns: <https://linked.data.gov.au/def/csdm/commonpatterns/> .
@prefix ex:             <https://linked.data.gov.au/def/csdm/examples/commonpatterns/> .
@prefix rdfs:           <http://www.w3.org/2000/01/rdf-schema#> .

# A survey point with a quality class and a numeric quality measure, as produced by the
# ptQuality / ptQualityMeasure properties of the Survey Features schema.
ex:surveyPoint1
  rdfs:label "PM 12345" ;
  commonpatterns:qualityClass ex:class-b ;
  commonpatterns:qualityMeasure 0.02 ;
.

# A qualified measurement: a value with a quality measure.
ex:distance1
  a commonpatterns:Measure ;
  commonpatterns:value 101.234 ;
  commonpatterns:qualityMeasure 0.005 ;
.

```

## Sources

* [CSDM Common Patterns module (icsm-au/3d-csdm, csdm_model/commonpatterns.ttl)](https://github.com/icsm-au/3d-csdm/blob/main/csdm_model/commonpatterns.ttl)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/surroundaustralia/3d-csdm-model](https://github.com/surroundaustralia/3d-csdm-model)
* Path: `_sources/model/commonpatterns`

