
# CSDM Survey Features (Model)

`icsm.csdm.model.surveyfeatures` *v0.1*

Feature types defined by cadastral surveys (survey marks, boundaries, monuments etc.).

[*Status*](http://www.opengis.net/def/status): Under development

## Examples

### survey features examples
Example data from `csdm_model/examples/survey_features_examples.ttl`.
#### turtle
```turtle
# baseURI: https://linked.data.gov.au/dataset/csdm/surveyfeatures-examples
# imports: https://linked.data.gov.au/def/csdm/surveyfeatures.shapes
# imports: https://data.surroundaustralia.com/def/ontexamples/shapes
# imports: https://www.opengis.net/def/csdm/examples/codelists/surveymark_condition_NZ

@prefix : <https://linked.data.gov.au/dataset/csdm/surveyfeatures-examples/> .
@prefix com: <https://w3id.org/ogc/utils/label/> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix nameparttype: <https://linked.data.gov.au/def/csdm/examples/nameparttypes/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix geometry: <https://linked.data.gov.au/def/csdm/geometry/> .
@prefix gml: <http://www.opengis.net/ont/gml#> .
@prefix metadata: <http://topbraid.org/metadata#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix prof: <http://www.w3.org/ns/dx/prof/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sf: <http://www.opengis.net/ont/sf#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix surv: <https://linked.data.gov.au/def/csdm/surveyfeatures/> .
@prefix surveymark_condition_NZ: <https://www.opengis.net/def/csdm/examples/codelists/surveymark_condition_NZ/> .
@prefix survprov: <https://linked.data.gov.au/def/csdm/surveyprov/> .
@prefix teamwork: <http://topbraid.org/teamwork#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://data.surroundaustralia.com/cadastre-3d/surveyobs/Distance>
  foaf:depiction <https://surroundbitbucket.bitbucket.io/3d-cadastre/images/scale_factor.png> ;
.
<https://linked.data.gov.au/dataset/csdm/surveyfeatures-examples>
  a owl:Ontology ;
  owl:imports <https://linked.data.gov.au/def/csdm/surveyfeatures.shapes> ;
  owl:imports <https://data.surroundaustralia.com/def/ontexamples/shapes> ;
  owl:imports <https://www.opengis.net/def/csdm/examples/codelists/surveymark_condition_NZ> ;
.
:SurveyExample
  a survprov:CSD ;
  rdfs:label "Survey 1 submitted CSD" ;
  prov:endedAtTime "2020-06-22"^^xsd:date ;
  prov:generated :SurveyExample ;
  prov:wasAssociatedWith <https://linked.data.gov.au/dataset/csdm//surveyactivity/examples/LandOnlineNZ> ;
  prov:wasAttributedTo <https://linked.data.gov.au/dataset/csdm//surveyactivity/examples/AH> ;
  prov:wasGeneratedBy <https://linked.data.gov.au/dataset/csdm//surveyactivity/examples/SurveyLodged_1> ;
  prov:wasInfluencedBy <https://linked.data.gov.au/dataset/csdm//surveyactivity/examples/SurveyApproval_1> ;
.
:g_p1
  a gml:Point ;
  geo:asGML """ <gml:Point gml:id=\"g_p1\" srsName=\"*XY-MT*\" srsDimension=\"3\">
                       <gml:pos>-31.596 38.089 5.000</gml:pos>
                    </gml:Point>"""^^geo:gmlLiteral ;
  rdfs:label "p1 location" ;
.
:g_p10
  a gml:Point ;
  geo:asGML """ <gml:Point gml:id=\"g_p10\" srsName=\"*XY-MT*\" srsDimension=\"3\">
                       <gml:pos>-33.717 43.089 4.550</gml:pos>
                    </gml:Point>"""^^geo:gmlLiteral ;
  rdfs:label "p10 location" ;
.
:g_p25
  a gml:Point ;
  geo:asGML """ <gml:Point gml:id=\"p25\" srsName=\"*XY-MT*\" srsDimension=\"3\">
                        <gml:pos>45.089 -38.596 -0.100</gml:pos>
                    </gml:Point>"""^^geo:gmlLiteral ;
  rdfs:label "p25 location" ;
.
:m25
  a surv:Monument ;
  rdfs:label "IS II" ;
  surv:condition surveymark_condition_NZ:Reliable ;
.
:p25
  a surv:BoundaryMark ;
  geo:hasGeometry :g_p25 ;
  rdfs:label "P25" ;
  com:name [
      a com:CompoundName ;
      dct:hasPart [
          a com:NamePart ;
          com:namePartType nameparttype:Source ;
          rdfs:label "DP 333333" ;
        ] ;
      dct:hasPart [
          a com:NamePart ;
          com:namePartType nameparttype:Stamp ;
          rdfs:label "IS II" ;
        ] ;
    ] ;
  surv:monumentedBy :m25 ;
  surv:purpose surveymark_condition_NZ:bound ;
  surv:state surveymark_condition_NZ:New ;
.
surv:BoundaryMark
  skos:example :p25 ;
.
surv:Monument
  skos:example :m25 ;
.
surv:SurveyPoint
  skos:example :p25 ;
.
[
  a prof:ResourceDescriptor ;
  dct:conformsTo <http://landxml.org/> ;
  dct:format "text/xml" ;
  rdfs:label "LandXML (12D) encoding" ;
  prof:hasArtifact "<Monument name=\"IT X DP 333333\" pntRef=\"101\" desc=\"IT X DP 333333\" type=\"tube\" condition=\"reliable\" oID=\"5828822\"/>" ;
  prof:hasRole <http://www.w3.org/ns/dx/prof/role/example> ;
].

```


### survmark condition NZ
Example data from `csdm_model/examples/survmark_condition_NZ.ttl`.
#### turtle
```turtle
# baseURI: https://www.opengis.net/def/csdm/examples/codelists/surveymark_condition_NZ
# imports: http://www.w3.org/2004/02/skos/core
# imports: https://w3id.org/ogc/utils/label
# imports: https://linked.data.gov.au/def/csdm/surveyfeatures.shapes

@prefix : <https://www.opengis.net/def/csdm/examples/codelists/surveymark_condition_NZ/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix surv: <https://linked.data.gov.au/def/csdm/surveyfeatures/> .
@prefix unnamed: <https://www.opengis.net/def/profiles/unnamed#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://www.opengis.net/def/csdm/examples/codelists/surveymark_condition_NZ>
  a owl:Ontology ;
  owl:imports <http://www.w3.org/2004/02/skos/core> ;
  owl:imports <https://w3id.org/ogc/utils/label> ;
  owl:imports <https://linked.data.gov.au/def/csdm/surveyfeatures.shapes> ;
  owl:versionInfo "Created with TopBraid Composer" ;
.
:Damaged
  a surv:ConditionCode ;
  rdfs:label "Damaged" ;
.
:New
  a surv:SurveyPointState ;
  rdfs:label "New" ;
.
:Original
  a surv:SurveyPointState ;
  rdfs:label "Original" ;
.
:Reliable
  a surv:MonumentCondition ;
  rdfs:label "Reliable" ;
.
:SurveyMarkCondition_NZ
  a surv:SurveyMarkCondition ;
  rdfs:label "NZ Survey Mark Condition Codes" ;
  skos:hasTopConcept :Damaged ;
  skos:hasTopConcept :Reliable ;
.
:bound
  a surv:SurveyPointPurpose ;
  rdfs:label "boundary defined by survey" ;
.
:ironspike
  a surv:MonumentForm ;
  rdfs:label "Iron Spike" ;
.
:nonbound
  a surv:SurveyPointPurpose ;
  rdfs:label "non-boundary" ;
.

```

## Sources

* [3D CSDM model source (icsm-au/3d-csdm)](https://github.com/icsm-au/3d-csdm/tree/main/csdm_model)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/surroundaustralia/3d-csdm-model](https://github.com/surroundaustralia/3d-csdm-model)
* Path: `_sources/model/surveyfeatures`

