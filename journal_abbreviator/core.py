"""ISO 4 abbreviation with a built-in subset of the List of Title Word Abbreviations (LTWA).

LTWA entries ending in '-' are stems: 'biolog-' matches biology, biological, biologist...
Words not in the list are kept in full, as ISO 4 requires.
"""
import json
import re

# A practical subset of the ISSN LTWA covering words common in scientific journal titles.
LTWA = {
    "academ-": "Acad.", "acta": "Acta", "advanc-": "Adv.", "agricult-": "Agric.", "america-": "Am.",
    "analy-": "Anal.", "anatom-": "Anat.", "animal": "Anim.", "annal-": "Ann.", "annual": "Annu.",
    "anthropolog-": "Anthropol.", "appli-": "Appl.", "archaeolog-": "Archaeol.", "architect-": "Archit.",
    "archiv-": "Arch.", "artificial": "Artif.", "association": "Assoc.", "astronom-": "Astron.",
    "astrophys-": "Astrophys.", "bacteriolog-": "Bacteriol.", "behavio-": "Behav.", "biochem-": "Biochem.",
    "biolog-": "Biol.", "biomedic-": "Biomed.", "biotechnolog-": "Biotechnol.", "botan-": "Bot.",
    "british": "Br.", "bulletin": "Bull.", "canad-": "Can.", "cancer": "Cancer", "cardiolog-": "Cardiol.",
    "cell-": "Cell.", "cellular": "Cell.", "chemi-": "Chem.", "child-": "Child.", "chin-": "Chin.",
    "clinic-": "Clin.", "cognit-": "Cogn.", "communica-": "Commun.", "comparat-": "Comp.",
    "computa-": "Comput.", "computer-": "Comput.", "conference": "Conf.", "conservation": "Conserv.",
    "current": "Curr.", "dermatolog-": "Dermatol.", "design": "Des.", "develop-": "Dev.",
    "diabet-": "Diabetes", "disease": "Dis.", "ecolog-": "Ecol.", "econom-": "Econ.", "educat-": "Educ.",
    "electr-": "Electr.", "electronic": "Electron.", "endocrinolog-": "Endocrinol.", "energ-": "Energy",
    "engineer-": "Eng.", "environment-": "Environ.", "epidemiolog-": "Epidemiol.", "europe-": "Eur.",
    "evolution-": "Evol.", "experiment-": "Exp.", "food": "Food", "frontier-": "Front.", "gastroenterolog-": "Gastroenterol.",
    "general": "Gen.", "genetic-": "Genet.", "geograph-": "Geogr.", "geolog-": "Geol.", "geophys-": "Geophys.",
    "health": "Health", "histor-": "Hist.", "hospital": "Hosp.", "human": "Hum.", "immunolog-": "Immunol.",
    "industr-": "Ind.", "infect-": "Infect.", "informat-": "Inf.", "institut-": "Inst.", "intelligen-": "Intell.",
    "interdisciplin-": "Interdiscip.", "international": "Int.", "investigat-": "Investig.", "japan-": "Jpn.",
    "journal": "J.", "laborator-": "Lab.", "language": "Lang.", "learning": "Learn.", "letter-": "Lett.",
    "linguist-": "Linguist.", "machine": "Mach.", "magazine": "Mag.", "management": "Manag.",
    "material-": "Mater.", "mathemat-": "Math.", "measurement": "Meas.", "mechani-": "Mech.",
    "medic-": "Med.", "methods": "Methods", "microbiolog-": "Microbiol.", "molecul-": "Mol.",
    "monthly": "Mon.", "national": "Natl.", "natur-": "Nat.", "network-": "Netw.", "neural": "Neural",
    "neurolog-": "Neurol.", "neurosci-": "Neurosci.", "nuclear": "Nucl.", "nutrition-": "Nutr.",
    "oncolog-": "Oncol.", "operation-": "Oper.", "optic-": "Opt.", "organi-": "Org.", "pathol-": "Pathol.",
    "pattern": "Pattern", "pediatr-": "Pediatr.", "pharmac-": "Pharm.", "pharmacolog-": "Pharmacol.",
    "philosoph-": "Philos.", "physic-": "Phys.", "physiolog-": "Physiol.", "planetary": "Planet.",
    "polic-": "Policy", "politic-": "Polit.", "polymer-": "Polym.", "practic-": "Pract.", "proceeding-": "Proc.",
    "process-": "Process.", "psychiatr-": "Psychiatry", "psycholog-": "Psychol.", "public": "Public",
    "quarterly": "Q.", "radiolog-": "Radiol.", "recognition": "Recognit.", "report-": "Rep.",
    "research": "Res.", "review-": "Rev.", "robotic-": "Robot.", "royal": "R.", "scien-": "Sci.",
    "scientific": "Sci.", "series": "Ser.", "signal": "Signal", "social": "Soc.", "societ-": "Soc.",
    "sociolog-": "Sociol.", "software": "Softw.", "statist-": "Stat.", "studies": "Stud.", "study": "Stud.",
    "surg-": "Surg.", "survey-": "Surv.", "system-": "Syst.", "technical": "Tech.", "techni-": "Tech.",
    "technolog-": "Technol.", "theor-": "Theor.", "therap-": "Ther.", "transaction-": "Trans.",
    "trend-": "Trends", "university": "Univ.", "veterinar-": "Vet.", "virolog-": "Virol.", "zoolog-": "Zool.",
}
# Articles, conjunctions and prepositions are omitted (ISO 4 section 7).
OMIT = set("a an the of and for in on at to by with from de des du la le les der die das und et y e el".split())
_TOKEN = re.compile(r"[A-Za-zÀ-ɏ]+(?:'[A-Za-z]+)?|[^A-Za-zÀ-ɏ\s]+")


class Abbreviator:
    def __init__(self, extra=None, overrides=None):
        """extra: additional LTWA-style word rules; overrides: whole-title -> abbreviation."""
        self.words = {k.lower(): v for k, v in LTWA.items()}
        self.words.update({k.lower(): v for k, v in (extra or {}).items()})
        self.overrides = {k.lower(): v for k, v in (overrides or {}).items()}
        self.stems = sorted((k[:-1] for k in self.words if k.endswith("-")), key=len, reverse=True)

    @classmethod
    def from_json(cls, path):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        return cls(data.get("words"), data.get("titles"))

    def word(self, w):
        lw = w.lower()
        if lw in self.words:
            return self.words[lw]
        for s in self.stems:
            if lw.startswith(s):
                return self.words[s + "-"]
        return w

    def abbreviate(self, title):
        """Abbreviate a journal title. Single-word titles are never abbreviated (ISO 4 rule)."""
        clean = " ".join(title.replace("&", " and ").split())
        if clean.lower() in self.overrides:
            return self.overrides[clean.lower()]
        tokens = _TOKEN.findall(clean)
        words = [t for t in tokens if t[0].isalpha()]
        if len(words) <= 1:
            return clean
        out = []
        for i, t in enumerate(tokens):
            if not t[0].isalpha():
                if t in (":", ";") or t.startswith("("):
                    out.append(t)
                continue
            if t.lower() in OMIT and i != 0:
                continue
            if t.lower() in OMIT and i == 0 and len(words) > 1 and t.lower() in ("the", "a", "an"):
                continue
            ab = self.word(t)
            if ab == t and t.isupper() and len(t) > 1:
                out.append(t)          # acronyms such as IEEE, ACM, BMJ stay as they are
            else:
                out.append(ab if ab != t else t[0].upper() + t[1:])
        text = " ".join(out)
        return re.sub(r"\s+([:;])", r"\1", text)


_default = None


def abbreviate(title):
    global _default
    if _default is None:
        _default = Abbreviator()
    return _default.abbreviate(title)
