# journal-abbreviator

**Abbreviate journal titles to ISO 4 (`Journal of the American Chemical Society` ->
`J. Am. Chem. Soc.`) for single titles or entire `.bib` files.**

Part of the *Research Automation Toolkit*: 100 open tools for daily research work.

## Why

Many journals (chemistry, physics, medicine, IEEE) require abbreviated journal names in the
reference list. Looking each one up is tedious and reference managers are inconsistent. ISO 4
defines the rules, and the ISSN List of Title Word Abbreviations (LTWA) defines the word forms.

## Features

- ISO 4 rules: omit articles/prepositions/conjunctions, abbreviate words by LTWA stem
  (`biolog-` covers biology, biological ...), keep single-word titles (`Nature`) unabbreviated
- Built-in LTWA subset of ~180 frequent scientific title words; acronyms (IEEE, ACM) preserved
- Custom rules JSON: extra words and whole-title overrides (`PLOS ONE` -> `PLoS One`)
- Rewrites only `journal` fields in BibTeX; reads titles from arguments or stdin

## Usage

```bash
pip install .
journal-abbreviator "Proceedings of the National Academy of Sciences"
journal-abbreviator --bib refs.bib -o refs_abbrev.bib --rules my_rules.json
cat journals.txt | journal-abbreviator
```

Rules file format:

```json
{"words": {"zebrafish": "Zebrafish", "nanotechnolog-": "Nanotechnol."},
 "titles": {"PLOS ONE": "PLoS One"}}
```

The built-in table is a subset; verify unusual titles against the official LTWA
(https://www.issn.org/services/online-services/access-to-the-ltwa/).

## Testing

```bash
python -m unittest discover -s tests -t .
```

## License

MIT (c) JANIN A APURBA
