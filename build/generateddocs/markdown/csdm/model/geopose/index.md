
# CSDM GeoPose (Model)

`icsm.csdm.model.geopose` *v0.1*

RDF terms for the GeoPose Basic-YPR structure (position and yaw, pitch, roll angles) used by 3D CSDM survey observation results.

[*Status*](http://www.opengis.net/def/status): Under development

## Examples

### Pose of a survey vector observation result
The RDF form of `hasResult.pose` in the 3d-csdm-common CSD example: yaw and pitch angles.
#### turtle
```turtle
@prefix geopose: <https://linked.data.gov.au/def/csdm/utils/geopose/> .
@prefix surv:    <https://linked.data.gov.au/def/csdm/surveyfeatures/> .
@prefix ex:      <https://linked.data.gov.au/def/csdm/examples/geopose/> .

# The pose of a survey vector observation result, from the 3d-csdm-common CSD example (hasResult.pose).
ex:result1
  surv:pose [
      geopose:angles [
          geopose:yaw 231.38 ;
          geopose:pitch -0.001 ;
        ] ;
    ] ;
.

```

## Sources

* [OGC GeoPose](https://www.ogc.org/standards/geopose/)
* [3D CSDM common: SurveyObservations schema](https://github.com/surroundaustralia/3d-csdm-common/tree/main/_sources/csdm/features/SurveyObservations)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/surroundaustralia/3d-csdm-model](https://github.com/surroundaustralia/3d-csdm-model)
* Path: `_sources/model/geopose`

