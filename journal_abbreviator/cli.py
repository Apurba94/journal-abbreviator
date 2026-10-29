"""Command-line interface for journal-abbreviator."""
import argparse
import re
import sys

from .core import Abbreviator


def abbreviate_bib(text, ab, field="journal"):
    """Replace journal = {...} values in BibTeX text; returns (new_text, changes)."""
    changes = []

    def repl(m):
        new = ab.abbreviate(m.group(3))
        if new != m.group(3):
            changes.append((m.group(3), new))
        return m.group(1) + m.group(2) + new + m.group(4)
    pattern = re.compile(r"(\b%s\s*=\s*)([{\"])([^{}\"]+)([}\"])" % field, re.IGNORECASE)
    return pattern.sub(repl, text), changes


def main(argv=None):
    ap = argparse.ArgumentParser(prog="journal-abbreviator", description="ISO 4 journal title abbreviation.")
    ap.add_argument("titles", nargs="*", help="journal titles to abbreviate")
    ap.add_argument("--bib", help="abbreviate the journal fields of this .bib file")
    ap.add_argument("-o", "--output", help="output .bib (default: print changes only)")
    ap.add_argument("--rules", help="JSON with {'words': {...}, 'titles': {...}} custom rules")
    args = ap.parse_args(argv)

    ab = Abbreviator.from_json(args.rules) if args.rules else Abbreviator()
    for t in args.titles:
        print("%s -> %s" % (t, ab.abbreviate(t)))
    if not args.titles and not args.bib:
        for line in sys.stdin:
            if line.strip():
                print(ab.abbreviate(line.strip()))
    if args.bib:
        with open(args.bib, encoding="utf-8") as fh:
            new, changes = abbreviate_bib(fh.read(), ab)
        for old, abbr in sorted(set(changes)):
            print("%s -> %s" % (old, abbr))
        if args.output:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(new)
    return 0
