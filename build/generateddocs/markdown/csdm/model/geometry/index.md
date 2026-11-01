
# CSDM Geometry Primitives (Model)

`icsm.csdm.model.geometry` *v0.1*

Extends GeoSPARQL with a named subset of ISO 19107 concepts for 3D solids and 3D topology amongst features. A candidate extension for GeoSPARQL 1.1. Includes the former GeoSPARQL 3D profile placeholder module, and maps its terms to the Topo-Feature and spatial-representation ontologies used by the exchange encoding.

[*Status*](http://www.opengis.net/def/status): Under development

## Examples

### geometryprimitives examples
Example data from `csdm_model/examples/geometryprimitives_examples.ttl`.
#### turtle
```turtle
# baseURI: https://www.opengis.net/def/csdm/geometryprimitives/examples/
# imports: https://linked.data.gov.au/def/csdm/geometry.shapes
# imports: https://data.surroundaustralia.com/def/ontexamples/shapes
# prefix: examples

@prefix examples: <https://www.opengis.net/def/csdm/geometryprimitives/examples/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix geometry: <https://linked.data.gov.au/def/csdm/geometry/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

examples:
  a owl:Ontology ;
  owl:imports <https://linked.data.gov.au/def/csdm/geometry.shapes> ;
  owl:imports <https://data.surroundaustralia.com/def/ontexamples/shapes> ;
  owl:versionInfo "Created with TopBraid Composer" ;
.
examples:ExtensionRule_1
  a <https://linked.data.gov.au/def/csdm/geometry/ExtensionRule> ;
  geometry:extension 1000.0 ;
  geometry:isOutward true ;
  rdfs:label "ExtrudedSurface_Implicit" ;
.
examples:ExtrudedSurface_1
  a <https://linked.data.gov.au/def/csdm/geometry/ExtrudedSurface> ;
  geo:asGML """<gml:Polygon gml:id=\"blue_top\">
                        <gml:exterior>
                            <gml:LinearRing gml:id=\"lr1\">
                                <gml:pointProperty xlink:href=\"#p1\"/>
                                <gml:pointProperty xlink:href=\"#p4\"/>
                                <gml:pointProperty xlink:href=\"#p3\"/>
                                <gml:pointProperty xlink:href=\"#p2\"/>
                                <gml:pointProperty xlink:href=\"#p1\"/>
                            </gml:LinearRing>
                        </gml:exterior>
                    </gml:Polygon>"""^^geo:gmlLiteral ;
  geo:dimension 3 ;
  rdfs:comment "Example with no explicit extrusion information - implement system rules will apply based on surface orientation (e.g. centre of earth to 1000 metres above ground level)" ;
  rdfs:label "ExtrudedSurface_Implicit" ;
.
examples:ExtrudedSurface_2
  a <https://linked.data.gov.au/def/csdm/geometry/ExtrudedSurface> ;
  geo:asGML """<gml:Polygon gml:id=\"blue_top\">
                        <gml:exterior>
                            <gml:LinearRing gml:id=\"lr1\">
                                <gml:pointProperty xlink:href=\"#p1\"/>
                                <gml:pointProperty xlink:href=\"#p4\"/>
                                <gml:pointProperty xlink:href=\"#p3\"/>
                                <gml:pointProperty xlink:href=\"#p2\"/>
                                <gml:pointProperty xlink:href=\"#p1\"/>
                            </gml:LinearRing>
                        </gml:exterior>
                    </gml:Polygon>"""^^geo:gmlLiteral ;
  geo:dimension 3 ;
  rdfs:comment "Example with explicit upward extrusion limit information - the implicit downward extension is 0" ;
  rdfs:label "ExtrudedSurface_Explicit" ;
  <https://linked.data.gov.au/def/csdm/geometry/limit> examples:ExtensionRule_1 ;
.

```

## Sources

* [3D CSDM model source (icsm-au/3d-csdm)](https://github.com/icsm-au/3d-csdm/tree/main/csdm_model)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/surroundaustralia/3d-csdm-model](https://github.com/surroundaustralia/3d-csdm-model)
* Path: `_sources/model/geometry`

