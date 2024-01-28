#! python3

"""
Grammar checker tests for French language
"""

import unittest
import os
import re
import time
from contextlib import contextmanager


from ..graphspell.echo import echo
from . import gc_engine


@contextmanager
def timeblock (label, hDst):
    "performance counter (contextmanager)"
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print('{} : {}'.format(label, end - start))
        if hDst:
            hDst.write("{:<12.6}".format(end-start))


def perf (sVersion, sResultFile=""):
    "performance tests"
    print("Performance tests")
    gc_engine.load()
    gc_engine.parse("Text to compile rules before launching real tests.")

    spHere, _ = os.path.split(__file__)
    spfPerfTest = os.path.join(spHere, "perf.txt")
    if not os.path.exists(spfPerfTest):
        print(f"No file <perf.txt> in <{spHere}>")
        return
    with open(spfPerfTest, "r", encoding="utf-8") as hSrc:
        hDst = open(sResultFile, "a", encoding="utf-8", newline="\n")  if sResultFile  else None
        if hDst:
            hDst.write("{:<12}{:<20}".format(sVersion, time.strftime("%Y.%m.%d %H:%M")))
        for sText in ( s.strip() for s in hSrc if not s.startswith("#") and s.strip() ):
            with timeblock(sText[:sText.find(".")], hDst):
                gc_engine.parse(sText)
        if hDst:
            hDst.write("\n")


def _fuckBackslashUTF8 (s):
    "fuck that shit"
    return s.replace("\u2019", "'").replace("\u2013", "–").replace("\u2014", "—")


class TestGrammarChecking (unittest.TestCase):
    "Tests du correcteur grammatical"

    @classmethod
    def setUpClass (cls):
        gc_engine.load()
        cls._zError = re.compile(r"\{\{.*?\}\}")
        cls._zRuleEnd = re.compile(r"_a\d+_\d+$")
        cls._aTestedRules = set()
        cls._oSpellChecker = gc_engine.getSpellChecker()

    def test_parse (self):
        zOption = re.compile("^__([a-zA-Z0-9]+)__ ")
        spHere, _ = os.path.split(__file__)
        spfParsingTest = os.path.join(spHere, "gc_test.txt")
        if not os.path.exists(spfParsingTest):
            print(f"No file <gc_test.txt> in <{spHere}>")
            return
        with open(spfParsingTest, "r", encoding="utf-8") as hSrc:
            nUnexpectedErrors = 0
            nTestWithExpectedError = 0
            nTestWithExpectedErrorAndSugg = 0
            for sLine in ( s for s in hSrc if not s.startswith("#") and s.strip() ):
                sLineNum = sLine[:10].strip()
                sLine = sLine[10:].strip()
                sOption = None
                m = zOption.search(sLine)
                if m:
                    sLine = sLine[m.end():]
                    sOption = m.group(1)
                if "->>" in sLine:
                    sErrorText, sExceptedSuggs = self._splitTestLine(sLine)
                    nTestWithExpectedErrorAndSugg += 1
                else:
                    sErrorText = sLine.strip()
                    sExceptedSuggs = ""
                sExpectedErrors = self._getExpectedErrors(sErrorText)
                if sExpectedErrors.strip() != "":
                    nTestWithExpectedError += 1
                sTextToCheck = sErrorText.replace("}}", "").replace("{{", "")
                sFoundErrors, sListErr, sFoundSuggs = self._getFoundErrors(sTextToCheck, sOption)
                # tests
                if sExpectedErrors != sFoundErrors:
                    print("\n# Line num: " + sLineNum + \
                          "\n> to check: " + _fuckBackslashUTF8(sTextToCheck) + \
                          "\n  expected: " + sExpectedErrors + \
                          "\n  found:    " + sFoundErrors + \
                          "\n  errors:   \n" + sListErr)
                    nUnexpectedErrors += 1
                elif sExceptedSuggs:
                    if not self._checkSuggestions(sExceptedSuggs, sFoundSuggs):
                        print("\n# Line num: " + sLineNum + \
                              "\n> to check: " + _fuckBackslashUTF8(sTextToCheck) + \
                              "\n  expected: " + sExceptedSuggs + \
                              "\n  found:    " + sFoundSuggs + \
                              "\n  errors:   \n" + sListErr)
                        nUnexpectedErrors += 1
            print("Tests with expected errors:", nTestWithExpectedError, " and suggestions:", nTestWithExpectedErrorAndSugg, "> {:.4} %".format(nTestWithExpectedErrorAndSugg/nTestWithExpectedError*100))
            if nUnexpectedErrors:
                print("Unexpected errors:", nUnexpectedErrors)
            self._showUntestedRules()

    def _showUntestedRules (self):
        aUntestedRules = set()
        for _, sOpt, sLineId, sRuleId in gc_engine.listRules():
            sRuleId = sRuleId.rstrip("0123456789")
            if sOpt != "@@@@" and sRuleId not in self._aTestedRules and not re.search("^[0-9]+[sp]$|^[pd]_", sRuleId):
                aUntestedRules.add(f"{sLineId}/{sRuleId}")
        if aUntestedRules:
            print()
            for sRule in sorted(aUntestedRules):
                echo(sRule)
            echo("  [{} untested rules]".format(len(aUntestedRules)))

    def _splitTestLine (self, sLine):
        sText, sSugg = sLine.split("->>")
        sSugg = sSugg.strip()
        if sSugg.startswith('"') and sSugg.endswith('"'):
            sSugg = sSugg[1:-1]
        return (sText.strip(), sSugg)

    def _getFoundErrors (self, sLine, sOption):
        if sOption:
            gc_engine.setOption(sOption, True)
            aErrs = gc_engine.parse(sLine)
            gc_engine.setOption(sOption, False)
        else:
            aErrs = gc_engine.parse(sLine)
        sRes = " " * len(sLine)
        sListErr = ""
        lAllSugg = []
        for dErr in sorted(aErrs, key=lambda d: d["nStart"]):
            sRes = sRes[:dErr["nStart"]] + "~" * (dErr["nEnd"] - dErr["nStart"]) + sRes[dErr["nEnd"]:]
            sListErr += "    * {sLineId} / {sRuleId}  at  {nStart}:{nEnd}\n".format(**dErr)
            lAllSugg.append("|".join(dErr["aSuggestions"]))
            self._aTestedRules.add(dErr["sRuleId"].rstrip("0123456789"))
            # test messages
            aGramErrs = gc_engine.parse(purgeMessage(dErr["sMessage"]))
            aGramErrs = [ dMsgErr  for dMsgErr in sorted(aGramErrs, key=lambda d: d["nStart"])  if self._zRuleEnd.sub("", dMsgErr["sRuleId"]) != self._zRuleEnd.sub("", dErr["sRuleId"]) ]
            aSpellErrs = self._oSpellChecker.parseParagraph(re.sub("‹[^›]+›", lambda m: " " * len(m.group(0)), dErr["sMessage"]))
            if aGramErrs or aSpellErrs or "<start>" in dErr["sMessage"] or "<end>" in dErr["sMessage"]:
                print("\n# Error in: <" + dErr["sMessage"] + ">\n    " + dErr["sLineId"] + " / " + dErr["sRuleId"])
                for dMsgErr in aGramErrs:
                    print("        error: {sLineId} / {sRuleId}  at  {nStart}:{nEnd}".format(**dMsgErr))
                for dMsgErr in aSpellErrs:
                    print("        spelling mistake: <{sValue}>  at  {nStart}:{nEnd}".format(**dMsgErr))
        return sRes, sListErr, "|||".join(lAllSugg)

    def _getExpectedErrors (self, sLine):
        sRes = " " * len(sLine)
        for i, m in enumerate(self._zError.finditer(sLine)):
            nStart = m.start() - (4 * i)
            nEnd = m.end() - (4 * (i+1))
            sRes = sRes[:nStart] + "~" * (nEnd - nStart) + sRes[nEnd:-4]
        return sRes

    def _checkSuggestions (self, sAllExceptedSuggs, sAllFoundSuggs):
        lAllExpectedSuggs = sAllExceptedSuggs.split("|||")
        lAllFoundSuggs = sAllFoundSuggs.split("|||")
        if len(lAllExpectedSuggs) != len(lAllFoundSuggs):
            return False
        for sExceptedSuggs, sFoundSuggs in zip(lAllExpectedSuggs, lAllFoundSuggs):
            lExpectedSuggs = sExceptedSuggs.split("|")
            lFoundSuggs = sFoundSuggs.split("|")
            if len(lExpectedSuggs) != len(lFoundSuggs) or set(lExpectedSuggs) != set(lFoundSuggs):
                return False
        return True


def purgeMessage (sMessage):
    "remove space after elided French words"
    for sToReplace, sReplacement in [
        ("l’ ", "l’"), ("d’ ", "d’"), ("n’ ", "n’"), ("j’ ", "j’"), ("m’ ", "m’"), ("t’ ", "t’"), ("s’ ", "s’"), ("qu’ ", "qu’"),
        ("L’ ", "L’"), ("D’ ", "D’"), ("N’ ", "N’"), ("J’ ", "J’"), ("M’ ", "M’"), ("T’ ", "T’"), ("S’ ", "S’"), ("QU’ ", "QU’")
    ]:
        sMessage = sMessage.replace(sToReplace, sReplacement)
    return sMessage


def main():
    "start function"
    unittest.main()


if __name__ == '__main__':
    main()
