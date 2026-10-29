import json
import os
import tempfile
import unittest

from journal_abbreviator.cli import abbreviate_bib, main
from journal_abbreviator.core import Abbreviator, abbreviate


class AbbreviateTests(unittest.TestCase):
    def test_well_known_titles(self):
        cases = {
            "Journal of the American Chemical Society": "J. Am. Chem. Soc.",
            "Proceedings of the National Academy of Sciences": "Proc. Natl. Acad. Sci.",
            "Physical Review Letters": "Phys. Rev. Lett.",
            "Journal of Biological Chemistry": "J. Biol. Chem.",
            "Annual Review of Psychology": "Annu. Rev. Psychol.",
            "International Journal of Molecular Sciences": "Int. J. Mol. Sci.",
        }
        for full, short in cases.items():
            self.assertEqual(abbreviate(full), short, full)

    def test_single_word_titles_unchanged(self):
        self.assertEqual(abbreviate("Nature"), "Nature")
        self.assertEqual(abbreviate("  Science "), "Science")

    def test_acronyms_and_unknown_words_kept(self):
        self.assertEqual(abbreviate("IEEE Transactions on Pattern Analysis and Machine Intelligence"),
                         "IEEE Trans. Pattern Anal. Mach. Intell.")
        self.assertEqual(abbreviate("Journal of Zebrafish Things"), "J. Zebrafish Things")

    def test_ampersand_and_colon(self):
        self.assertEqual(abbreviate("Research & Policy: Annual Review"), "Res. Policy: Annu. Rev.")

    def test_custom_rules(self):
        ab = Abbreviator(extra={"zebrafish": "Zebrafish", "thing-": "Thg."}, overrides={"PLOS ONE": "PLoS One"})
        self.assertEqual(ab.abbreviate("Journal of Zebrafish Things"), "J. Zebrafish Thg.")
        self.assertEqual(ab.abbreviate("plos one"), "PLoS One")

    def test_bib_rewrite_and_cli(self):
        text = "@article{a, journal = {Journal of Applied Physics}, title={Journal of Applied Physics}}"
        new, changes = abbreviate_bib(text, Abbreviator())
        self.assertIn("journal = {J. Appl. Phys.}", new)
        self.assertIn("title={Journal of Applied Physics}", new)
        self.assertEqual(changes, [("Journal of Applied Physics", "J. Appl. Phys.")])
        with tempfile.TemporaryDirectory() as d:
            src, out, rules = (os.path.join(d, n) for n in ("in.bib", "out.bib", "r.json"))
            with open(src, "w", encoding="utf-8") as fh:
                fh.write(text)
            with open(rules, "w", encoding="utf-8") as fh:
                json.dump({"titles": {"Journal of Applied Physics": "JAP"}}, fh)
            main(["--bib", src, "-o", out, "--rules", rules])
            with open(out, encoding="utf-8") as fh:
                self.assertIn("journal = {JAP}", fh.read())


if __name__ == "__main__":
    unittest.main()
