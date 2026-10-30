The Cadastral Parcels module of the 3D CSDM (`https://linked.data.gov.au/def/csdm/parcels`).

The OGC [Land Parcels ontology](https://ogcincubator.github.io/bblocks-land-parcels/bblock/ogc.ladm.land-parcels.ontology)
(`https://w3id.org/ogc/ladm/parcels`) was derived from this module and is declared as a dependency, so that the two can be
reconciled (for example by the CSDM re-using the land-parcels terms, or declaring equivalences).

## Reconciliation with the Land Parcels ontology

The comparison below ignores namespace IRIs: CSDM and land-parcels terms with the same local name are treated as the same
concept, and only differences in their definitions are listed. It was generated with `tools/reconcile-parcels.sh`; the
machine-readable form is in [`reconciliation/differences.csv`](reconciliation/differences.csv).

### Namespace mappings (IRI differences ignored)

| token | CSDM | land-parcels |
|---|---|---|
| `parcel:` | `https://linked.data.gov.au/def/csdm/parcels/` | `https://w3id.org/ogc/ladm/parcels/` |
| `com:` | `https://w3id.org/ogc/utils/label/` | `https://w3id.org/ogc/utils/label/` (unchanged) |
| `geometry:` | `https://linked.data.gov.au/def/csdm/geometry/` | `https://linked.data.gov.au/def/csdm/geometry/` (unchanged) |

### Concept differences

The CSDM declares 31 terms in the parcels namespace, and land-parcels has the same terms except `ParcelModel`. Of the 30 shared
terms, 26 are identical (labels, definitions, notes, examples, domains, ranges, restrictions and images). The other 4 differ
only in their `ParcelModel` superclass. The only real change is that land-parcels removed the `ParcelModel` grouping class:

| concept | kind | change | property | CSDM value | land-parcels value |
|---|---|---|---|---|---|
| `parcel:ParcelModel` | Class | only in CSDM | `rdf:type` | `owl:Class` | — |
| `parcel:ParcelModel` | Class | only in CSDM | `rdfs:subClassOf` | `owl:Thing` | — |
| `parcel:ParcelModel` | Class | only in CSDM | `skos:prefLabel` | "Parcel Module Component"@en | — |
| `parcel:Appellation` | Class | differs | `rdfs:subClassOf` | `parcel:ParcelModel` | — |
| `parcel:LandInterest` | Class | differs | `rdfs:subClassOf` | `parcel:ParcelModel` | — |
| `parcel:Parcel` | Class | differs | `rdfs:subClassOf` | `parcel:ParcelModel` | — |
| `parcel:ParcelAggregate` | Class | differs | `rdfs:subClassOf` | `parcel:ParcelModel` | — |

### Points to resolve

1. **`ParcelModel` removal is incomplete in land-parcels.** `parcel:CodeTypes rdfs:subClassOf parcel:ParcelModel` is still
   there, so land-parcels refers to a class it no longer declares. Either restore `ParcelModel` or remove that last
   reference too.
2. **`com:` terms (resolved).** Both ontologies now use `com:name` and `com:RelevantJurisdictionalCodelist` from
   `https://w3id.org/ogc/utils/label/`. These terms are declared in the Common Patterns ontology
   (`ogc.bbr.utils.commonpatterns`) in the [Utility](https://ogcincubator.github.io/bblocks-utility/) register. That ontology
   was previously the CSDM Common Patterns module. The land-parcels ontology block now declares
   `ogc.bbr.utils.commonpatterns` in its `dependsOn`.
3. **`geometry:` still points at the CSDM.** land-parcels uses `geometry:3DSpatialUnit` and `geometry:hasGeometryPart` in
   the CSDM geometry namespace, so it implicitly depends on CSDM Geometry Primitives (`icsm.csdm.model.geometry`).
4. **Problems shared by both sources** (copied over unchanged, to be fixed in both):
   - `parcel:Parcel sh:property parcel:Parcel-parcelType` refers to a property shape that neither ontology declares
     (the CSDM declares it in `parcel_module.shapes.ttl`).
   - `parcel:PurposeOfSpatialUnit rdfs:subClassOf <urn:x-evn-master:file_parcels_ttl/CodeTypes>` is a TopBraid EDG
     working-copy IRI; it should be `parcel:CodeTypes`.
   - `sdo:address rdfs:Label "Address"` uses `rdfs:Label`, which should be `rdfs:label`, and the definition re-declares a
     schema.org term inside the parcels ontology.
   - `parcel:floor` has no `rdf:type` (it should be an `owl:DatatypeProperty` or `owl:ObjectProperty`).
   - Leading spaces in the labels `" Estate"`, `" Estate Parcel"`, `" Interest In Land"`.
