#!python3

"""
INDEXABLE BINARY DIRECT ACYCLIC WORD GRAPH
Implementation of a spellchecker as a transducer (storing transformation code to get lemma and morphologies)
and a spell suggestion mechanism
"""

import traceback
import pkgutil
import re
from functools import wraps
import time
import json
import binascii
import importlib
from collections import OrderedDict
from math import floor

#import logging
#logging.basicConfig(filename="suggestions.log", level=logging.DEBUG)

from . import str_transform as st
from . import char_player as cp
from .echo import echo


def timethis (func):
    "decorator for the execution time"
    @wraps(func)
    def wrapper (*args, **kwargs):
        "something to prevent pylint whining"
        fStart = time.time()
        result = func(*args, **kwargs)
        fEnd = time.time()
        print(func.__name__, fEnd - fStart)
        return result
    return wrapper


class SuggResult:
    """Structure for storing, classifying and filtering suggestions"""

    def __init__ (self, sWord, nSuggLimit=10, nDistLimit=-1):
        self.sWord = sWord
        self.sSimplifiedWord = st.simplifyWord(sWord)
        self.nDistLimit = nDistLimit  if nDistLimit >= 0  else  (len(sWord) // 3) + 1
        self.nMinDist = 1000
        # Temporary sets
        self.aAllSugg = set()   # All suggestions, even the one rejected
        self.dGoodSugg = {}     # Acceptable suggestions
        self.dBestSugg = {}     # Best suggestions
        # Parameters
        self.nSuggLimit = nSuggLimit
        self.nSuggLimitExt = nSuggLimit + 2             # we add few entries in case suggestions merge after casing modifications
        self.nBestSuggLimit = floor(nSuggLimit * 2)     # n times the requested limit
        self.nGoodSuggLimit = nSuggLimit * 15           # n times the requested limit

    def addSugg (self, sSugg, nDeep=0):
        "add a suggestion"
        if sSugg in self.aAllSugg:
            return
        self.aAllSugg.add(sSugg)
        nDistJaro = 1 - st.distanceJaroWinkler(self.sSimplifiedWord, st.simplifyWord(sSugg))
        nDist = floor(nDistJaro * 10)
        if nDist < self.nMinDist:
            self.nMinDist = nDist
        #logging.info((nDeep * "  ") + "__" + sSugg + "__ " + str(round(nDistJaro*1000)))
        if nDistJaro < .11:     # Best suggestions
            self.dBestSugg[sSugg] = round(nDistJaro*1000)
            if len(self.dBestSugg) > self.nBestSuggLimit:
                self.nDistLimit = -1  # make suggest() to end search
        elif nDistJaro < .33:   # Good suggestions
            self.dGoodSugg[sSugg] = round(nDistJaro*1000)
            if len(self.dGoodSugg) > self.nGoodSuggLimit:
                self.nDistLimit = -1  # make suggest() to end search
        self.nDistLimit = min(self.nDistLimit, self.nMinDist+1)

    def getSuggestions (self):
        "return a list of suggestions"
        # we sort the better results with the original word
        lRes = []
        if len(self.dBestSugg) > 0:
            # sort only with simplified words
            lResTmp = sorted(self.dBestSugg.items(), key=lambda x: x[1])
            for i in range(min(self.nSuggLimitExt, len(lResTmp))):
                lRes.append(lResTmp[i][0])
        if len(lRes) < self.nSuggLimitExt:
            # sort with simplified words and original word
            lResTmp = sorted(self.dGoodSugg.items(), key=lambda x: ((1-st.distanceJaroWinkler(self.sWord, x[0]))*10, x[1]))
            for i in range(min(self.nSuggLimitExt, len(lResTmp))):
                lRes.append(lResTmp[i][0])
        # casing
        if self.sWord.isupper():
            lRes = list(OrderedDict.fromkeys(map(lambda sSugg: sSugg.upper(), lRes))) # use dict, when Python 3.6+
        elif self.sWord[0:1].isupper():
            # dont’ use <.istitle>
            lRes = list(OrderedDict.fromkeys(map(lambda sSugg: sSugg[0:1].upper()+sSugg[1:], lRes))) # use dict, when Python 3.6+
        return lRes[:self.nSuggLimit]


class IBDAWG:
    """INDEXABLE BINARY DIRECT ACYCLIC WORD GRAPH"""

    def __init__ (self, source):
        if isinstance(source, str):
            by = pkgutil.get_data(__package__, "_dictionaries/" + source)
            if not by:
                raise OSError("# Error. File not found or not loadable: "+source)
            self.sFileName = source
            oData = json.loads(by.decode("utf-8"))     #json.loads(by)    # In Python 3.6, can read directly binary strings
        else:
            self.sFileName = "[None]"
            oData = source

        self.__dict__.update(oData)
        self.dCharVal = { v: k  for k, v in self.dChar.items() }
        self.a2grams = set(getattr(self, 'l2grams'))  if hasattr(self, 'l2grams')  else None

        if "lByDic" not in oData:
            print(">>>> lByDic not in oData")
            if "sByDic" not in oData:
                raise TypeError("# Error. No usable data in the dictionary.")
            # old dictionary version
            self.lByDic = []
            self.byDic = binascii.unhexlify(oData["sByDic"])
            nAcc = 0
            byBuffer = b""
            nDivisor = (self.nBytesArc + self.nBytesNodeAddress) / 2
            for i in range(0, len(self.byDic)):
                byBuffer += self.byDic[i:i+1]
                if nAcc == (self.nBytesArc - 1):
                    self.lByDic.append(int.from_bytes(byBuffer, byteorder="big"))
                    byBuffer = b""
                elif nAcc == (self.nBytesArc + self.nBytesNodeAddress - 1):
                    self.lByDic.append(round(int.from_bytes(byBuffer, byteorder="big") / nDivisor))
                    byBuffer = b""
                    nAcc = -1
                nAcc = nAcc + 1

        # masks
        self._arcMask = (2 ** ((self.nBytesArc * 8) - 3)) - 1
        self._finalNodeMask = 1 << ((self.nBytesArc * 8) - 1)
        self._lastArcMask = 1 << ((self.nBytesArc * 8) - 2)

        # function to decode the affix/suffix code
        if self.cStemming == "S":
            self.funcStemming = st.changeWordWithSuffixCode
        elif self.cStemming == "A":
            self.funcStemming = st.changeWordWithAffixCode
        else:
            self.funcStemming = st.noStemming

        self.bAcronymValid = False
        self.bNumAtLastValid = False

        # lexicographer module ?
        self.lexicographer = None
        try:
            self.lexicographer = importlib.import_module(".lexgraph_"+self.sLangCode, "grammalecte.graphspell")
        except ImportError:
            print("# No module <graphspell.lexgraph_"+self.sLangCode+".py>")

    def getInfo (self):
        "return string about the IBDAWG"
        return  "  Language: {0.sLangName}   Lang code: {0.sLangCode}   Dictionary name: {0.sDicName}" \
                "  Date: {0.sDate}   Stemming: {0.cStemming}FX\n" \
                "  Arcs values:  {0.nArcVal:>10,} = {0.nChar:>5,} characters,  {0.nAff:>6,} affixes,  {0.nTag:>6,} tags\n" \
                "  Dictionary: {0.nEntry:>12,} entries,    {0.nNode:>11,} nodes,   {0.nArc:>11,} arcs\n" \
                "  Address size: {0.nBytesNodeAddress:>1} bytes,  Arc size: {0.nBytesArc:>1} bytes\n".format(self)

    def isValidToken (self, sToken):
        "checks if <sToken> is valid (if there is hyphens in <sToken>, <sToken> is split, each part is checked)"
        sToken = st.spellingNormalization(sToken)
        if self.isValid(sToken):
            return True
        if "-" in sToken:
            if sToken.count("-") > 4:
                return True
            return all(self.isValid(sWord)  for sWord in sToken.split("-"))
        if "." in sToken or "·" in sToken:
            return True
        return False

    def isValid (self, sWord):
        "checks if <sWord> is valid (different casing tested if the first letter is a capital)"
        if not sWord:
            return True
        if self.lookup(sWord):
            return True
        if sWord[0:1].isupper():
            if len(sWord) > 1:
                if sWord.istitle():
                    return self.lookup(sWord.lower())
                if sWord.isupper():
                    return self.bAcronymValid or self.lookup(sWord.lower()) or self.lookup(sWord.capitalize())
                return self.lookup(sWord[:1].lower() + sWord[1:])
            return self.lookup(sWord.lower())
        if sWord[0:1].isdigit():
            return True
        return False

    def lookup (self, sWord):
        "returns True if <sWord> in dictionary (strict verification)"
        iAddr = 0
        for c in sWord:
            if c not in self.dChar:
                return False
            iAddr = self._lookupArcNode(self.dChar[c], iAddr)
            if iAddr is None:
                return False
        return bool(self.lByDic[iAddr] & self._finalNodeMask)

    def getMorph (self, sWord):
        "retrieves morphologies list, different casing allowed"
        if not sWord:
            return []
        sWord = st.spellingNormalization(sWord)
        l = self._morph(sWord)
        if sWord[0:1].isupper():
            l.extend(self._morph(sWord.lower()))
            if sWord.isupper() and len(sWord) > 1:
                l.extend(self._morph(sWord.capitalize()))
        return l

    #@timethis
    def suggest (self, sWord, nSuggLimit=10, bSplitTrailingNumbers=False):
        "returns a set of suggestions for <sWord>"
        sWord = sWord.rstrip(".")   # useful for LibreOffice
        sWord = st.spellingNormalization(sWord)
        sPfx = ""
        sSfx = ""
        if self.lexicographer:
            sPfx, sWord, sSfx = self.lexicographer.split(sWord)
        nMaxSwitch = max(len(sWord) // 3, 1)
        nMaxDel = len(sWord) // 5
        nMaxHardRepl = max((len(sWord) - 5) // 4, 1)
        nMaxJump = max(len(sWord) // 4, 1)
        oSuggResult = SuggResult(sWord, nSuggLimit)
        sWord = st.cleanWord(sWord)
        if bSplitTrailingNumbers:
            self._splitTrailingNumbers(oSuggResult, sWord)
        self._splitSuggest(oSuggResult, sWord)
        self._suggest(oSuggResult, sWord)
        self._suggest(oSuggResult, sWord, nMaxSwitch, nMaxDel, nMaxHardRepl, nMaxJump)
        aSugg = oSuggResult.getSuggestions()
        if sSfx or sPfx:
            # we add what we removed
            return list(map(lambda sSug: sPfx + sSug + sSfx, aSugg))
        return aSugg

    def _splitTrailingNumbers (self, oSuggResult, sWord):
        m = re.match(r"(\D+)([0-9]+)$", sWord)
        if m and m.group(1)[-1:].isalpha():
            oSuggResult.addSugg(m.group(1) + " " + st.numbersToExponent(m.group(2)))

    def _splitSuggest (self, oSuggResult, sWord):
        # split at apostrophes
        for cSplitter in "'’":
            if cSplitter in sWord:
                sWord1, sWord2 = sWord.split(cSplitter, 1)
                if self.isValid(sWord1) and self.isValid(sWord2):
                    oSuggResult.addSugg(sWord1+" "+sWord2)

    def _suggest (self, oSuggResult, sRemain, nMaxSwitch=0, nMaxDel=0, nMaxHardRepl=0, nMaxJump=0, nDist=0, nDeep=0, iAddr=0, sNewWord="", bAvoidLoop=False):
        # recursive function
        #logging.info((nDeep * "  ") + sNewWord + ":" + sRemain)
        if self.lByDic[iAddr] & self._finalNodeMask:
            if not sRemain:
                oSuggResult.addSugg(sNewWord, nDeep)
                for sTail in self._getTails(iAddr):
                    oSuggResult.addSugg(sNewWord+sTail, nDeep)
                return
            if (len(sNewWord) + len(sRemain) == len(oSuggResult.sWord)) and oSuggResult.sWord.lower().startswith(sNewWord.lower()) and self.isValid(sRemain):
                if self.sLangCode == "fr" and sNewWord.lower() in ("l", "d", "n", "m", "t", "s", "c", "j", "qu", "lorsqu", "puisqu", "quoiqu", "jusqu", "quelqu") and sRemain[0:1] in cp.aVowel:
                    oSuggResult.addSugg(sNewWord+"’"+sRemain, nDeep)
                if (len(sNewWord) > 1 and len(sRemain) > 1) or sNewWord in "aày" or sRemain in "aày":
                    oSuggResult.addSugg(sNewWord+" "+sRemain, nDeep)
        if nDist > oSuggResult.nDistLimit:
            return
        cCurrent = sRemain[0:1]
        for cChar, jAddr in self._getCharArcs(iAddr):
            if cChar in cp.d1to1.get(cCurrent, cCurrent):
                self._suggest(oSuggResult, sRemain[1:], nMaxSwitch, nMaxDel, nMaxHardRepl, nMaxJump, nDist, nDeep+1, jAddr, sNewWord+cChar)
            elif not bAvoidLoop:
                if nMaxHardRepl and self.isNgramsOK(cChar+sRemain[1:2]):
                    self._suggest(oSuggResult, sRemain[1:], nMaxSwitch, nMaxDel, nMaxHardRepl-1, nMaxJump, nDist+1, nDeep+1, jAddr, sNewWord+cChar, True)
                if nMaxJump:
                    self._suggest(oSuggResult, sRemain, nMaxSwitch, nMaxDel, nMaxHardRepl, nMaxJump-1, nDist+1, nDeep+1, jAddr, sNewWord+cChar, True) # True for avoiding loop?
        if not bAvoidLoop: # avoid infinite loop
            if len(sRemain) > 1:
                if cCurrent == sRemain[1:2]:
                    # same char, we remove 1 char without adding 1 to <sNewWord>
                    self._suggest(oSuggResult, sRemain[1:], nMaxSwitch, nMaxDel, nMaxHardRepl, nMaxJump, nDist, nDeep+1, iAddr, sNewWord)
                else:
                    # switching chars
                    if nMaxSwitch and self.isNgramsOK(sNewWord[-1:]+sRemain[1:2]) and self.isNgramsOK(sRemain[1:2]+sRemain[0:1]):
                        self._suggest(oSuggResult, sRemain[1:2]+sRemain[0:1]+sRemain[2:], nMaxSwitch-1, nMaxDel, nMaxHardRepl, nMaxJump, nDist+1, nDeep+1, iAddr, sNewWord, True)
                    # delete char
                    if nMaxDel and self.isNgramsOK(sNewWord[-1:]+sRemain[1:2]):
                        self._suggest(oSuggResult, sRemain[1:], nMaxSwitch, nMaxDel-1, nMaxHardRepl, nMaxJump, nDist+1, nDeep+1, iAddr, sNewWord, True)
                # Phonetic replacements
                for sRepl in cp.get1toXReplacement(sNewWord[-1:], cCurrent, sRemain[1:2]):
                    self._suggest(oSuggResult, sRepl + sRemain[1:], nMaxSwitch, nMaxDel, nMaxHardRepl, nMaxJump, nDist, nDeep+1, iAddr, sNewWord, True)
                for sRepl in cp.d2toX.get(sRemain[0:2], ()):
                    self._suggest(oSuggResult, sRepl + sRemain[2:], nMaxSwitch, nMaxDel, nMaxHardRepl, nMaxJump, nDist, nDeep+1, iAddr, sNewWord, True)
            # end of word
            if len(sRemain) == 2:
                for sRepl in cp.dFinal2.get(sRemain, ()):
                    self._suggest(oSuggResult, sRepl, nMaxSwitch, nMaxDel, nMaxHardRepl, nMaxJump, nDist, nDeep+1, iAddr, sNewWord, True)
            elif len(sRemain) == 1:
                self._suggest(oSuggResult, "", nMaxSwitch, nMaxDel, nMaxHardRepl, nMaxJump, nDist, nDeep+1, iAddr, sNewWord, True) # remove last char and go on
                for sRepl in cp.dFinal1.get(sRemain, ()):
                    self._suggest(oSuggResult, sRepl, nMaxSwitch, nMaxDel, nMaxHardRepl, nMaxJump, nDist, nDeep+1, iAddr, sNewWord, True)

    def isNgramsOK (self, sChars):
        "returns True if sChars in known 2grams"
        if len(sChars) != 2:
            return True
        if not self.a2grams:
            return True
        return sChars in self.a2grams

    def _getCharArcs (self, iAddr):
        "generator: yield all chars and addresses from node at address <iAddr>"
        for nVal, jAddr in self._getArcs(iAddr):
            if nVal <= self.nChar:
                yield (self.dCharVal[nVal], jAddr)

    def _getTails (self, iAddr, sTail="", n=2):
        "return a list of suffixes ending at a distance of <n> from <iAddr>"
        aTails = set()
        for nVal, jAddr in self._getArcs(iAddr):
            if nVal <= self.nChar:
                if self.lByDic[jAddr] & self._finalNodeMask:
                    aTails.add(sTail + self.dCharVal[nVal])
                if n and not aTails:
                    aTails.update(self._getTails(jAddr, sTail+self.dCharVal[nVal], n-1))
        return aTails

    def drawPath (self, sWord, iAddr=0):
        "show the path taken by <sWord> in the graph"
        sWord = st.spellingNormalization(sWord)
        c1 = sWord[0:1]  if sWord  else " "
        iPos = -1
        n = 0
        echo(c1 + ": ", end="")
        for c2, jAddr in self._getCharArcs(iAddr):
            echo(c2, end="")
            if c2 == sWord[0:1]:
                iNextNodeAddr = jAddr
                iPos = n
            n += 1
        if not sWord:
            return
        if iPos >= 0:
            echo("\n   " + " " * iPos + "|")
            self.drawPath(sWord[1:], iNextNodeAddr)

    def getSimilarEntries (self, sWord, nSuggLimit=10):
        "return a list of tuples (similar word, stem, morphology)"
        if not sWord:
            return []
        lResult = []
        for sSimilar in self.suggest(sWord, nSuggLimit):
            for sMorph in self.getMorph(sSimilar):
                nCut = sMorph.find("/")
                lResult.append( (sSimilar, sMorph[1:nCut], sMorph[nCut+1:]) )
        return lResult

    def select (self, sFlexPattern="", sTagsPattern=""):
        "generator: returns all entries which flexion fits <sFlexPattern> and morphology fits <sTagsPattern>"
        zFlexPattern = None
        zTagsPattern = None
        try:
            if sFlexPattern:
                zFlexPattern = re.compile(sFlexPattern)
            if sTagsPattern:
                zTagsPattern = re.compile(sTagsPattern)
        except re.error:
            print("# Error in regex pattern")
            traceback.print_exc()
        yield from self._select(zFlexPattern, zTagsPattern, 0, "")

    def _select (self, zFlexPattern, zTagsPattern, iAddr, sWord):
        # recursive generator
        for nVal, jAddr in self._getArcs(iAddr):
            if nVal <= self.nChar:
                # simple character
                yield from self._select(zFlexPattern, zTagsPattern, jAddr, sWord + self.lArcVal[nVal])
            else:
                if not zFlexPattern or zFlexPattern.search(sWord):
                    sStem = self.funcStemming(sWord, self.lArcVal[nVal])
                    for nMorphVal, _ in self._getArcs(jAddr):
                        if not zTagsPattern or zTagsPattern.search(self.lArcVal[nMorphVal]):
                            yield [sWord, sStem, self.lArcVal[nMorphVal]]

    def _morph (self, sWord):
        "returns morphologies of <sWord>"
        iAddr = 0
        for c in sWord:
            if c not in self.dChar:
                return []
            iAddr = self._lookupArcNode(self.dChar[c], iAddr)
            if iAddr is None:
                return []
        if self.lByDic[iAddr] & self._finalNodeMask:
            l = []
            nRawArc = 0
            while not nRawArc & self._lastArcMask:
                iEndArcAddr = iAddr + 1
                nRawArc = self.lByDic[iAddr]
                nArc = nRawArc & self._arcMask
                if nArc > self.nChar:
                    # This value is not a char, this is a stemming code
                    sStem = ">" + self.funcStemming(sWord, self.lArcVal[nArc])
                    # Now , we go to the next node and retrieve all following arcs values, all of them are tags
                    iAddr2 = self.lByDic[iEndArcAddr]
                    nRawArc2 = 0
                    while not nRawArc2 & self._lastArcMask:
                        iEndArcAddr2 = iAddr2 + 1
                        nRawArc2 = self.lByDic[iAddr2]
                        l.append(sStem + "/" + self.lArcVal[nRawArc2 & self._arcMask])
                        iAddr2 = iEndArcAddr2 + 1
                iAddr = iEndArcAddr + 1
            return l
        return []

    def _stem (self, sWord):
        "returns stems list of <sWord>"
        iAddr = 0
        for c in sWord:
            if c not in self.dChar:
                return []
            iAddr = self._lookupArcNode(self.dChar[c], iAddr)
            if iAddr is None:
                return []
        if self.lByDic[iAddr] & self._finalNodeMask:
            l = []
            nRawArc = 0
            while not nRawArc & self._lastArcMask:
                iEndArcAddr = iAddr + 1
                nRawArc = self.lByDic[iAddr]
                nArc = nRawArc & self._arcMask
                if nArc > self.nChar:
                    # This value is not a char, this is a stemming code
                    l.append(self.funcStemming(sWord, self.lArcVal[nArc]))
                iAddr = iEndArcAddr + 1
            return l
        return []

    def _lookupArcNode (self, nVal, iAddr):
        "looks if <nVal> is an arc at the node at <iAddr>, if yes, returns address of next node else None"
        while True:
            iEndArcAddr = iAddr + 1
            nRawArc = self.lByDic[iAddr]
            if nVal == (nRawArc & self._arcMask):
                # the value we are looking for
                # we return the address of the next node
                return self.lByDic[iEndArcAddr]
            # value not found
            if nRawArc & self._lastArcMask:
                return None
            iAddr = iEndArcAddr + 1

    def _getArcs (self, iAddr):
        "generator: return all arcs at <iAddr> as tuples of (nVal, iAddr)"
        while True:
            iEndArcAddr = iAddr + 1
            nRawArc = self.lByDic[iAddr]
            yield nRawArc & self._arcMask, self.lByDic[iEndArcAddr]
            if nRawArc & self._lastArcMask:
                break
            iAddr = iEndArcAddr + 1

    def _writeNodes (self, spfDest):
        "for debugging only"
        print(" > Write binary nodes")
        with open(spfDest, 'w', 'utf-8', newline="\n") as hDst:
            iAddr = 0
            hDst.write("i{:_>10} -- #{:_>10}\n".format("0", iAddr))
            while iAddr < len(self.lByDic):
                iEndArcAddr = iAddr + 1
                nRawArc = self.lByDic[iAddr]
                nArc = nRawArc & self._arcMask
                hDst.write("  {:<20}  {:0>16}  i{:>10}   #{:_>10}\n".format(self.lArcVal[nArc], bin(nRawArc)[2:], "?", self.lByDic[iEndArcAddr]))
                iAddr = iEndArcAddr + 1
                if (nRawArc & self._lastArcMask) and iAddr < len(self.lByDic):
                    hDst.write("\ni{:_>10} -- #{:_>10}\n".format("?", iAddr))
            hDst.close()
