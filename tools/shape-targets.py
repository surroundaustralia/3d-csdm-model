#!/usr/bin/env python3
"""Add explicit class targets to the CSDM model SHACL shapes.

The model shapes are written as implicit class targets: a node shape whose IRI is the class it constrains. In SHACL
that only selects focus nodes if the shape is also declared an rdfs:Class in the shapes graph, which the shapes files
do not do, and even then it only reaches instances of subclasses if the rdfs:subClassOf statements are in the data
graph. As a result most model shapes never selected any focus node.

For every node shape whose IRI is a class declared in the model ontologies, this adds one generated line
    sh:targetClass <the class>, <each of its transitive subclasses> ;  # generated: tools/shape-targets.py
directly under its "a sh:NodeShape" line. A declared class that carries sh:property constraints but is not typed
sh:NodeShape (the TopBraid style, where the class itself holds the constraints) is not a shape at all, so it also gets
a generated "a sh:NodeShape" line. Re-running replaces the generated lines. Shapes named after classes that no
ontology declares are reported: they constrain nothing and should be removed or renamed.

Usage: shape-targets.py <ontology glob> <shapes file> [<shapes file> ...]
"""
import glob
import re
import sys
from collections import defaultdict

from rdflib import Graph, RDF, URIRef
from rdflib.namespace import OWL, RDFS, SH

MARK = '# generated: tools/shape-targets.py'

onto = Graph()
for f in glob.glob(sys.argv[1], recursive=True):
    if 'shapes' not in f and 'retired' not in f:
        onto.parse(f)
classes = {c for c in onto.subjects(RDF.type, OWL.Class) if isinstance(c, URIRef)} | \
          {c for c in onto.subjects(RDF.type, RDFS.Class) if isinstance(c, URIRef)}
subs = defaultdict(set)
for s, o in onto.subject_objects(RDFS.subClassOf):
    if isinstance(s, URIRef) and isinstance(o, URIRef):
        subs[o].add(s)


def closure(c):
    out, todo = {c}, [c]
    while todo:
        for s in subs.get(todo.pop(), ()):
            if s not in out:
                out.add(s)
                todo.append(s)
    return out


status = 0
for path in sys.argv[2:]:
    text = open(path, encoding='utf-8').read()
    # Previously generated lines are removed first, so the shapes are read as authored
    text = re.sub(r'\n[^\n]*' + re.escape(MARK), '', text)
    g = Graph().parse(data=text, format='turtle')
    nm = g.namespace_manager
    typed = {s for s in g.subjects(RDF.type, SH.NodeShape) if isinstance(s, URIRef)}
    untyped = {s for s in g.subjects(SH.property, None) if isinstance(s, URIRef) and s not in typed and s in classes}
    added, dead = 0, []
    for s in sorted(typed | untyped):
        if s not in classes:
            if not any((s, p, None) in g for p in (
                    SH.targetClass, SH.targetNode, SH.targetSubjectsOf, SH.targetObjectsOf, SH.target)):
                dead.append(s.n3(nm))
            continue
        targets = ', '.join(sorted(t.n3(nm) for t in closure(s)))
        subject = rf'(?:{re.escape(s.n3(nm))}|{re.escape(f"<{s}>")})'
        if s in typed:
            m = re.compile(rf'^({subject}\s*\n(\s+)a\s+sh:NodeShape\s*;)', re.M).search(text)
            lines = f'\n{{indent}}sh:targetClass {targets} ;  {MARK}'
        else:
            m = re.compile(rf'^({subject})\n(\s+)sh:property', re.M).search(text)
            lines = f'\n{{indent}}a sh:NodeShape ;  {MARK}\n{{indent}}sh:targetClass {targets} ;  {MARK}'
        if not m:
            print(f'  ! {path}: cannot locate the {s.n3(nm)} statement to add targets', file=sys.stderr)
            status = 1
            continue
        text = text[:m.end(1)] + lines.format(indent=m.group(2)) + text[m.end(1):]
        added += 1
    open(path, 'w', encoding='utf-8', newline='').write(text)
    print(f'{path}: targets added to {added} shapes')
    for d in dead:
        print(f'  untargeted shape (class not declared): {d}')
sys.exit(status)
