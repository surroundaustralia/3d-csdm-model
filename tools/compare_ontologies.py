#!/usr/bin/env python3
"""
Concept-level comparison of two ontologies, ignoring namespace IRIs.

Each input ontology is normalised by rewriting the IRIs of the given namespaces to a
neutral token (e.g. both `https://linked.data.gov.au/def/csdm/parcels/Parcel` and
`https://w3id.org/ogc/ladm/parcels/Parcel` become `parcel:Parcel`), so that only genuine
differences in concepts (declarations, labels, definitions, hierarchy, domains/ranges,
restrictions, annotations) remain. Blank-node structures are compared via canonical
isomorphism.

Usage:
  compare_ontologies.py SOURCE.ttl TARGET.ttl \
      --map parcel=https://linked.data.gov.au/def/csdm/parcels/,https://w3id.org/ogc/ladm/parcels/ \
      --map com=https://linked.data.gov.au/def/csdm/commonpatterns/,https://w3id.org/ogc/utils/label/ \
      --ont https://linked.data.gov.au/def/csdm/parcels,https://w3id.org/ogc/ladm/parcels \
      [--md out.md] [--csv out.csv]

`--map` namespaces are listed as SOURCE,TARGET. Whenever a mapped namespace differs between the
two ontologies this is reported separately, as it implies a change of module ownership rather
than a change of concept.
"""
import argparse
import csv
import sys
from collections import defaultdict

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.compare import graph_diff, to_isomorphic
from rdflib.namespace import OWL, RDF, RDFS, SKOS

NEUTRAL = 'urn:x-neutral:'


def load(path):
    g = Graph()
    g.parse(path, format='turtle')
    return g


def normaliser(maps, ont_iris, side):
    def norm(term):
        if isinstance(term, URIRef):
            s = str(term)
            if s in ont_iris or s.rstrip('/#') in ont_iris:
                return URIRef(NEUTRAL + 'ONTOLOGY')
            for token, namespaces in maps.items():
                ns = namespaces[side]
                if s.startswith(ns):
                    return URIRef(f'{NEUTRAL}{token}/{s[len(ns):]}')
        elif isinstance(term, Literal) and '\r' in term:
            # line endings in multi-line literals depend on how the source was checked out
            return Literal(str(term).replace('\r\n', '\n'), lang=term.language, datatype=term.datatype)
        return term
    return norm


def normalise(g, norm):
    out = Graph()
    for s, p, o in g:
        out.add((norm(s), norm(p), norm(o)))
    return out


class Shortener:
    def __init__(self, *graphs):
        self.nm = {}
        for g in graphs:
            for prefix, ns in g.namespaces():
                if prefix and str(ns) not in self.nm.values():
                    self.nm.setdefault(prefix, str(ns))

    def __call__(self, term):
        if isinstance(term, URIRef):
            s = str(term)
            if s.startswith(NEUTRAL):
                rest = s[len(NEUTRAL):]
                return '<ontology>' if rest == 'ONTOLOGY' else rest.replace('/', ':', 1)
            best = None
            for prefix, ns in self.nm.items():
                if s.startswith(ns) and (best is None or len(ns) > len(best[1])):
                    best = (prefix, ns)
            return f'{best[0]}:{s[len(best[1]):]}' if best else f'<{s}>'
        if isinstance(term, Literal):
            v = str(term).strip().replace('\n', ' ')
            if len(v) > 120:
                v = v[:117] + '...'
            suffix = f'@{term.language}' if term.language else ''
            return f'"{v}"{suffix}'
        return '[]'


def describe_bnode(g, b, short, depth=0):
    if depth > 2:
        return '[...]'
    parts = []
    for p, o in sorted(g.predicate_objects(b), key=lambda x: (str(x[0]), str(x[1]))):
        ov = describe_bnode(g, o, short, depth + 1) if isinstance(o, BNode) else short(o)
        parts.append(f'{short(p)} {ov}')
    return '[ ' + ' ; '.join(parts) + ' ]'


def kind_of(g, s):
    types = set(g.objects(s, RDF.type))
    for t, k in ((OWL.Class, 'Class'), (RDFS.Class, 'Class'), (OWL.ObjectProperty, 'ObjectProperty'),
                 (OWL.DatatypeProperty, 'DatatypeProperty'), (RDF.Property, 'Property'),
                 (OWL.Ontology, 'Ontology')):
        if t in types:
            return k
    return 'untyped'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source')
    ap.add_argument('target')
    ap.add_argument('--source-label', default='source')
    ap.add_argument('--target-label', default='target')
    ap.add_argument('--map', action='append', default=[], help='token=SOURCE_NS,TARGET_NS')
    ap.add_argument('--ont', default='', help='SOURCE_ONTOLOGY_IRI,TARGET_ONTOLOGY_IRI')
    ap.add_argument('--md')
    ap.add_argument('--csv')
    args = ap.parse_args()

    maps = {}
    for m in args.map:
        token, nss = m.split('=', 1)
        maps[token] = nss.split(',')
    ont_iris = set(i for i in args.ont.split(',') if i)

    g_src, g_tgt = load(args.source), load(args.target)
    n_src = normalise(g_src, normaliser(maps, ont_iris, 0))
    n_tgt = normalise(g_tgt, normaliser(maps, ont_iris, 1))
    short = Shortener(g_src, g_tgt)

    iso_src, iso_tgt = to_isomorphic(n_src), to_isomorphic(n_tgt)
    _, only_src, only_tgt = graph_diff(iso_src, iso_tgt)

    # Group diff triples by named subject (blank nodes are folded into their referencing subject)
    def group(diff, full):
        out = defaultdict(list)
        for s, p, o in diff:
            if isinstance(s, BNode):
                parents = list(full.subjects(None, s))
                if parents:
                    s = parents[0]
                    # the whole bnode will be reported via its parent link
                    if (s, None, None) in diff:
                        continue
            ov = describe_bnode(full, o, short) if isinstance(o, BNode) else short(o)
            out[s].append((short(p), ov))
        return out

    g_only_src, g_only_tgt = group(only_src, iso_src), group(only_tgt, iso_tgt)

    named = lambda g: {s for s in g.subjects() if isinstance(s, URIRef)}
    subj_src, subj_tgt = named(n_src), named(n_tgt)

    rows = []
    for s in sorted(set(g_only_src) | set(g_only_tgt), key=lambda x: short(x)):
        if s in subj_src and s not in subj_tgt:
            change = f'only in {args.source_label}'
        elif s in subj_tgt and s not in subj_src:
            change = f'only in {args.target_label}'
        else:
            change = 'differs'
        kind = kind_of(n_src, s) if s in subj_src else kind_of(n_tgt, s)
        for p, o in sorted(g_only_src.get(s, [])):
            rows.append((short(s), kind, change, p, o, ''))
        for p, o in sorted(g_only_tgt.get(s, [])):
            rows.append((short(s), kind, change, p, '', o))

    ns_rows = []
    for token, (ns_s, ns_t) in maps.items():
        if ns_s != ns_t:
            used_s = any(str(t).startswith(f'{NEUTRAL}{token}/') for tr in n_src for t in tr)
            used_t = any(str(t).startswith(f'{NEUTRAL}{token}/') for tr in n_tgt for t in tr)
            ns_rows.append((token, ns_s if used_s else '(unused)', ns_t if used_t else '(unused)'))

    # Terms in mapped namespaces that are referenced but never described, per side
    def dangling(g):
        mapped = lambda t: isinstance(t, URIRef) and str(t).startswith(NEUTRAL) and str(t) != NEUTRAL + 'ONTOLOGY'
        described = {s for s in g.subjects() if mapped(s)}
        used = {t for tr in g for t in (tr[1], tr[2]) if mapped(t)}
        return sorted((short(t) for t in used - described))
    dang_src, dang_tgt = dangling(n_src), dangling(n_tgt)

    if args.csv:
        with open(args.csv, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['concept', 'kind', 'change', 'property', f'{args.source_label} value',
                        f'{args.target_label} value'])
            w.writerows(rows)

    lines = [
        f'Compared **{args.source_label}** (`{args.source}`) with **{args.target_label}** (`{args.target}`).',
        '',
        f'- Triples: {len(g_src)} in {args.source_label}, {len(g_tgt)} in {args.target_label}',
        f'- Differing statements: {len(only_src)} only in {args.source_label}, '
        f'{len(only_tgt)} only in {args.target_label}',
        f'- Concepts affected: {len({r[0] for r in rows})}',
        '',
        '### Namespace mappings applied (IRI differences ignored)',
        '',
        f'| token | {args.source_label} | {args.target_label} |',
        '|---|---|---|',
    ]
    lines += [f'| `{t}:` | `{s}` | `{d}` |' for t, s, d in ns_rows]
    lines += [
        '',
        '### Concept differences',
        '',
        f'| concept | kind | change | property | {args.source_label} value | {args.target_label} value |',
        '|---|---|---|---|---|---|',
    ]
    esc = lambda v: v.replace('|', '\\|')
    lines += [f'| `{c}` | {k} | {ch} | `{p}` | {esc(a)} | {esc(b)} |' for c, k, ch, p, a, b in rows]
    lines += [
        '',
        '### Referenced but undeclared terms (mapped namespaces only)',
        '',
        f'| term | referenced in {args.source_label} | referenced in {args.target_label} |',
        '|---|---|---|',
    ]
    lines += [f'| `{t}` | {"yes" if t in dang_src else ""} | {"yes" if t in dang_tgt else ""} |'
              for t in sorted(set(dang_src) | set(dang_tgt))]
    md = '\n'.join(lines) + '\n'
    if args.md:
        with open(args.md, 'w', encoding='utf-8') as f:
            f.write(md)
    else:
        sys.stdout.write(md)


if __name__ == '__main__':
    main()
