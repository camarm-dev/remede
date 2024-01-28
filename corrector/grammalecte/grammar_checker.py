"""
Grammalecte, grammar checker
"""

import importlib
import json

from . import text


class GrammarChecker:
    "GrammarChecker: Wrapper for the grammar checker engine"

    def __init__ (self, sLangCode, sContext="Python"):
        self.sLangCode = sLangCode
        # Grammar checker engine
        self.gce = importlib.import_module("."+sLangCode, "grammalecte")
        self.gce.load(sContext)
        # Spell checker
        self.oSpellChecker = self.gce.getSpellChecker()
        # Lexicographer
        self.oLexicographer = None
        # Text formatter
        self.oTextFormatter = None

    def getGCEngine (self):
        "return the grammar checker object"
        return self.gce

    def getSpellChecker (self):
        "return the spell checker object"
        return self.oSpellChecker

    def getTextFormatter (self):
        "load and return the text formatter"
        if self.oTextFormatter is None:
            tf = importlib.import_module("."+self.sLangCode+".textformatter", "grammalecte")
            self.oTextFormatter = tf.TextFormatter()
        return self.oTextFormatter

    def getLexicographer (self):
        "load and return the lexicographer"
        if self.oLexicographer is None:
            lxg = importlib.import_module("."+self.sLangCode+".lexicographe", "grammalecte")
            self.oLexicographer = lxg.Lexicographe(self.oSpellChecker)
        return self.oLexicographer

    def displayGCOptions (self):
        "display the grammar checker options"
        self.gce.displayOptions()

    def getParagraphErrors (self, sText, dOptions=None, bContext=False, bSpellSugg=False, bDebug=False):
        "returns a tuple: (grammar errors, spelling errors)"
        aGrammErrs = self.gce.parse(sText, "FR", bDebug=bDebug, dOptions=dOptions, bContext=bContext)
        aSpellErrs = self.oSpellChecker.parseParagraph(sText, bSpellSugg)
        return aGrammErrs, aSpellErrs

    def getParagraphWithErrors (self, sText, dOptions=None, bEmptyIfNoErrors=False, bSpellSugg=False, nWidth=100, bDebug=False):
        "parse text and return a readable text with underline errors"
        aGrammErrs, aSpellErrs = self.getParagraphErrors(sText, dOptions, False, bSpellSugg, bDebug)
        if bEmptyIfNoErrors and not aGrammErrs and not aSpellErrs:
            return ("", [])
        return text.generateParagraph(sText, aGrammErrs, aSpellErrs, nWidth)

    def getTextWithErrors (self, sText, bEmptyIfNoErrors=False, bSpellSugg=False, nWidth=100, bDebug=False):
        "[todo]"

    def getParagraphErrorsAsJSON (self, iIndex, sText, dOptions=None, bContext=False, bEmptyIfNoErrors=False, bSpellSugg=False, bReturnText=False, lLineSet=None, bDebug=False):
        "parse text and return errors as a JSON string"
        aGrammErrs, aSpellErrs = self.getParagraphErrors(sText, dOptions, bContext, bSpellSugg, bDebug)
        aGrammErrs = list(aGrammErrs)
        if bEmptyIfNoErrors and not aGrammErrs and not aSpellErrs:
            return ""
        if lLineSet:
            aGrammErrs, aSpellErrs = text.convertToXY(aGrammErrs, aSpellErrs, lLineSet)
            return json.dumps({ "lGrammarErrors": aGrammErrs, "lSpellingErrors": aSpellErrs }, ensure_ascii=False)
        if bReturnText:
            return json.dumps({ "iParagraph": iIndex, "sText": sText, "lGrammarErrors": aGrammErrs, "lSpellingErrors": aSpellErrs }, ensure_ascii=False)
        return json.dumps({ "iParagraph": iIndex, "lGrammarErrors": aGrammErrs, "lSpellingErrors": aSpellErrs }, ensure_ascii=False)

    def getTextErrorsAsJSON (self, sText, bContext=False, bEmptyIfNoErrors=False, bSpellSugg=False, bReturnText=False, bDebug=False):
        "[todo]"
