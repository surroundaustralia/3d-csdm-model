Compared **CSDM** (`_sources/parcels/parcels.ttl`) with **land-parcels** (`https://raw.githubusercontent.com/ogcincubator/bblocks-land-parcels/master/_sources/ontology/parcels.ttl`).

- Triples: 174 in CSDM, 167 in land-parcels
- Differing statements: 7 only in CSDM, 0 only in land-parcels
- Concepts affected: 5

### Namespace mappings applied (IRI differences ignored)

| token | CSDM | land-parcels |
|---|---|---|
| `parcel:` | `https://linked.data.gov.au/def/csdm/parcels/` | `https://w3id.org/ogc/ladm/parcels/` |

### Concept differences

| concept | kind | change | property | CSDM value | land-parcels value |
|---|---|---|---|---|---|
| `parcel:Appellation` | Class | differs | `rdfs:subClassOf` | parcel:ParcelModel |  |
| `parcel:LandInterest` | Class | differs | `rdfs:subClassOf` | parcel:ParcelModel |  |
| `parcel:Parcel` | Class | differs | `rdfs:subClassOf` | parcel:ParcelModel |  |
| `parcel:ParcelAggregate` | Class | differs | `rdfs:subClassOf` | parcel:ParcelModel |  |
| `parcel:ParcelModel` | Class | only in CSDM | `rdf:type` | owl:Class |  |
| `parcel:ParcelModel` | Class | only in CSDM | `rdfs:subClassOf` | owl:Thing |  |
| `parcel:ParcelModel` | Class | only in CSDM | `skos:prefLabel` | "Parcel Module Component"@en |  |

### Referenced but undeclared terms (mapped namespaces only)

| term | referenced in CSDM | referenced in land-parcels |
|---|---|---|
| `com:RelevantJurisdictionalCodelist` | yes | yes |
| `com:name` | yes | yes |
| `geometry:3DSpatialUnit` | yes | yes |
| `parcel:Parcel-parcelType` | yes | yes |
| `parcel:ParcelModel` |  | yes |
