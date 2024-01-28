#! python3

"""
Grammar checker tests for French language
"""

import unittest
import time
from contextlib import contextmanager

from ..graphspell.spellchecker import SpellChecker
from . import conj
from . import phonet
from . import mfsp


@contextmanager
def timeblock (label, hDst=None):
    "performance counter (contextmanager)"
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print('{:<20} : {}'.format(label, end-start))
        if hDst:
            hDst.write("{:<12.6}".format(end-start))


class TestDictionary (unittest.TestCase):
    "Test du correcteur orthographique"

    @classmethod
    def setUpClass (cls):
        cls.oSpellChecker = SpellChecker("fr")

    def test_lookup (self):
        for sWord in ["branche", "Émilie"]:
            self.assertTrue(self.oSpellChecker.lookup(sWord), sWord)

    def test_lookup_failed (self):
        for sWord in ["Branche", "BRANCHE", "BranchE", "BRanche", "BRAnCHE", "émilie"]:
            self.assertFalse(self.oSpellChecker.lookup(sWord), sWord)

    def test_isvalidtoken (self):
        for sWord in ["Branche", "branche", "BRANCHE", "Émilie", "ÉMILIE", "aujourd'hui", "aujourd’hui", "Aujourd'hui", "Aujourd’hui", "je-suis-vraiment-fatigué", ""]:
            self.assertTrue(self.oSpellChecker.isValidToken(sWord), sWord)

    def test_isvalid (self):
        for sWord in ["Branche", "branche", "BRANCHE", "Émilie", "ÉMILIE", "aujourd’hui", "Aujourd’hui"]:
            self.assertTrue(self.oSpellChecker.isValid(sWord), sWord)

    def test_isvalid_failed (self):
        for sWord in ["BranchE", "BRanche", "BRAnCHE", "émilie", "éMILIE", "émiLie", "aujourd'hui", "Aujourd'hui", ]:
            self.assertFalse(self.oSpellChecker.isValid(sWord), sWord)

    def test_suggest (self):
        for sWrong, sSugg in [
            ("chassis", "châssis"),
            ("francais", "français"),
            ("déelirranttesss", "délirantes"),
            ("vallidasion", "validation"),
            ("Emilie", "Émilie"),
            ("exibission", "exhibition"),
            ("ditirembique", "dithyrambique"),
            ("jai", "j’ai"),
            ("email", "courriel"),
            ("fatiqué", "fatigué"),
            ("coeur", "cœur"),
            ("trèèèèèèèèès", "très"),
            ("vraaaaiiiimeeeeennnt", "vraiment"),
            ("apele", "appel"),
            ("Co2", "CO₂"),
            ("emmppâiiiller", "empailler"),
            ("testt", "test"),
            ("apelaion", "appellation"),
            ("exsepttion", "exception"),
            ("sintaxik", "syntaxique"),
            ("ebriete", "ébriété"),
            ("ennormmement", "énormément")
        ]:
            #with timeblock(sWord):
            for lSugg in self.oSpellChecker.suggest(sWrong):
                #print(sWord, "->", " ".join(lSugg))
                self.assertIn(sSugg, lSugg)


    def test_lemmas (self):
        for sWord, sInfi in [
            ("suis",        "suivre"),
            ("suis",        "être"),
            ("a",           "avoir"),
            ("a",           "a"),
            ("irai",        "aller"),
            ("jetez",       "jeter"),
            ("finit",       "finir"),
            ("mangé",       "manger"),
            ("oubliait",    "oublier"),
            ("arrivais",    "arriver"),
            ("venait",      "venir"),
            ("prendre",     "prendre")
        ]:
            self.assertIn(sInfi, self.oSpellChecker.getLemma(sWord))


class TestConjugation (unittest.TestCase):
    "Tests des conjugaisons"

    @classmethod
    def setUpClass (cls):
        pass

    def test_isverb (self):
        for sVerb in ["avoir", "être", "aller", "manger", "courir", "venir", "faire", "finir"]:
            self.assertTrue(conj.isVerb(sVerb), sVerb)
        for sVerb in ["berk", "a", "va", "contre", "super", "", "à"]:
            self.assertFalse(conj.isVerb(sVerb), sVerb)

    def test_hasconj (self):
        for sVerb, sTense, sWho in [("aller", ":E", ":2s"), ("avoir", ":Is", ":1s"), ("être", ":Ip", ":2p"),
                                    ("manger", ":Sp", ":3s"), ("finir", ":K", ":3p"), ("prendre", ":If", ":1p")]:
            self.assertTrue(conj.hasConj(sVerb, sTense, sWho), sVerb)

    def test_getconj (self):
        for sVerb, sTense, sWho, sConj in [("aller", ":E", ":2s", "va"), ("avoir", ":Iq", ":1s", "avais"), ("être", ":Ip", ":2p", "êtes"),
                                           ("manger", ":Sp", ":3s", "mange"), ("finir", ":K", ":3p", "finiraient"), ("prendre", ":If", ":1p", "prendrons")]:
            self.assertEqual(conj.getConj(sVerb, sTense, sWho), sConj, sVerb)


class TestPhonet (unittest.TestCase):
    "Tests des équivalences phonétiques"

    @classmethod
    def setUpClass (cls):
        cls.lSet = [
            ["ce", "se"],
            ["ces", "saie", "saies", "ses", "sais", "sait"],
            ["cet", "cette", "sept", "set", "sets"],
            ["dé", "dés", "dès", "dais", "des"],
            ["don", "dons", "dont"],
            ["été", "étaie", "étaies", "étais", "était", "étai", "étés", "étaient"],
            ["faire", "fer", "fers", "ferre", "ferres", "ferrent"],
            ["fois", "foi", "foie", "foies"],
            ["la", "là", "las"],
            ["mes", "mets", "met", "mai", "mais"],
            ["mon", "mont", "monts"],
            ["mot", "mots", "maux"],
            ["moi", "mois"],
            ["notre", "nôtre", "nôtres"],
            ["or", "ors", "hors"],
            ["hou", "houe", "houes", "ou", "où", "houx"],
            ["peu", "peux", "peut"],
            ["son", "sons", "sont"],
            ["tes", "tais", "tait", "taie", "taies", "thé", "thés"],
            ["toi", "toit", "toits"],
            ["ton", "tons", "thon", "thons", "tond", "tonds"],
            ["voir", "voire"]
        ]

    def test_getsimil (self):
        for aSet in self.lSet:
            for sWord in aSet:
                self.assertListEqual(phonet.getSimil(sWord), sorted(aSet))


class TestMasFemSingPlur (unittest.TestCase):
    "Tests des masculins, féminins, singuliers et pluriels"

    @classmethod
    def setUpClass (cls):
        cls.lPlural = [
            ("travail", ["travaux"]),
            ("vœu", ["vœux"]),
            ("gentleman", ["gentlemans", "gentlemen"])
        ]

    def test_getplural (self):
        for sSing, lPlur in self.lPlural:
            self.assertListEqual(mfsp.getMiscPlural(sSing), lPlur)


def main():
    "start function"
    unittest.main()


if __name__ == '__main__':
    main()
