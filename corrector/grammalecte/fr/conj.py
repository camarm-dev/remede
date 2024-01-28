"""
Grammalecte - Conjugueur
"""

# License: GPL 3

import re
import traceback

from .conj_data import lVtyp as _lVtyp
from .conj_data import lTags as _lTags
from .conj_data import dPatternConj as _dPatternConj
from .conj_data import dVerb as _dVerb
from .conj_data import dVerbNames as _dVerbNames


_zStartVoy = re.compile("^[aeéiouœê]")
_zNeedTeuph = re.compile("[tdc]$")
#_zNEEDACCENTWITHJE = re.compile("[^i]e$")

_dProSuj = { ":1s": "je", ":1ś": "je", ":2s": "tu", ":3s": "il", ":1p": "nous", ":2p": "vous", ":3p": "ils" }
_dProObj = { ":1s": "me ", ":1ś": "me ", ":2s": "te ", ":3s": "se ", ":1p": "nous ", ":2p": "vous ", ":3p": "se " }
_dProObjEl = { ":1s": "m’", ":1ś": "m’", ":2s": "t’", ":3s": "s’", ":1p": "nous ", ":2p": "vous ", ":3p": "s’" }
_dImpePro = { ":2s": "-toi", ":1p": "-nous", ":2p": "-vous" }
_dImpeProNeg = { ":2s": "ne te ", ":1p": "ne nous ", ":2p": "ne vous " }
_dImpeProEn = { ":2s": "-t’en", ":1p": "-nous-en", ":2p": "-vous-en" }
_dImpeProNegEn = { ":2s": "ne t’en ", ":1p": "ne nous en ", ":2p": "ne vous en " }

_dGroup = { "0": "auxiliaire", "1": "1ᵉʳ groupe", "2": "2ᵉ groupe", "3": "3ᵉ groupe" }

_dTenseIdx = { ":P": 0, ":Q": 1, ":Ip": 2, ":Iq": 3, ":Is": 4, ":If": 5, ":K": 6, ":Sp": 7, ":Sq": 8, ":E": 9 }



def isVerb (sVerb):
    "return True if it’s a existing verb"
    return sVerb in _dVerb


def getConj (sVerb, sTense, sWho):
    "returns conjugation (can be an empty string)"
    if sVerb not in _dVerb:
        return None
    if sTense == ":Y":
        return sVerb
    return _modifyStringWithSuffixCode(sVerb, _dPatternConj[sTense][_lTags[_dVerb[sVerb][1]][_dTenseIdx[sTense]]].get(sWho, ""))


def hasConj (sVerb, sTense, sWho):
    "returns False if no conjugation (also if empty) else True"
    if sVerb not in _dVerb:
        return False
    if sTense == ":Y" or _dPatternConj[sTense][_lTags[_dVerb[sVerb][1]][_dTenseIdx[sTense]]].get(sWho, False):
        return True
    return False


def getVtyp (sVerb):
    "returns raw informations about sVerb"
    if sVerb not in _dVerb:
        return None
    return _lVtyp[_dVerb[sVerb][0]]


def getNamesFrom (sVerb):
    "returns a list of names derivating from <sVerb>"
    if sVerb in _dVerbNames:
        # there are names derivated from the verb
        return list(_dVerbNames[sVerb])
    # nothing found: we suggest past participles
    tTags = _getTags(sVerb)
    if tTags:
        aSugg = [ _getConjWithTags(sVerb, tTags, ":Q", ":m:s") ]
        if _hasConjWithTags(tTags, ":Q", ":f:s"):
            aSugg.append(_getConjWithTags(sVerb, tTags, ":Q", ":f:s"))
        if _hasConjWithTags(tTags, ":Q", ":m:p"):
            aSugg.append(_getConjWithTags(sVerb, tTags, ":Q", ":m:p"))
        if _hasConjWithTags(tTags, ":Q", ":f:p"):
            aSugg.append(_getConjWithTags(sVerb, tTags, ":Q", ":f:p"))
        # if there is only one past participle (epi inv), unreliable.
        return aSugg  if len(aSugg) > 1  else []
    return []


def getConjSimilInfiV1 (sInfi):
    "returns verbal forms phonetically similar to infinitive form (for verb in group 1)"
    if sInfi not in _dVerb:
        return []
    aSugg = []
    tTags = _getTags(sInfi)
    if tTags:
        # example: arriver, arrivais, arrivait, arrivai, arrivez, arriviez
        if _hasConjWithTags(tTags, ":Iq", ":2s"):
            aSugg.append(_getConjWithTags(sInfi, tTags, ":Iq", ":2s"))
        if _hasConjWithTags(tTags, ":Iq", ":3s"):
            aSugg.append(_getConjWithTags(sInfi, tTags, ":Iq", ":3s"))
        if _hasConjWithTags(tTags, ":Iq", ":3p"):
            aSugg.append(_getConjWithTags(sInfi, tTags, ":Iq", ":3p"))
        if _hasConjWithTags(tTags, ":Is", ":1s"):
            aSugg.append(_getConjWithTags(sInfi, tTags, ":Is", ":1s"))
        if _hasConjWithTags(tTags, ":Ip", ":2p"):
            aSugg.append(_getConjWithTags(sInfi, tTags, ":Ip", ":2p"))
        if _hasConjWithTags(tTags, ":Iq", ":2p"):
            aSugg.append(_getConjWithTags(sInfi, tTags, ":Iq", ":2p"))
    return aSugg


def _getTags (sVerb):
    "returns tuple of tags (usable with functions _getConjWithTags and _hasConjWithTags)"
    if sVerb not in _dVerb:
        return None
    return _lTags[_dVerb[sVerb][1]]


def _getConjWithTags (sVerb, tTags, sTense, sWho):
    "returns conjugation (can be an empty string)"
    if sTense == ":Y":
        return sVerb
    return _modifyStringWithSuffixCode(sVerb, _dPatternConj[sTense][tTags[_dTenseIdx[sTense]]].get(sWho, ""))


def _hasConjWithTags (tTags, sTense, sWho):
    "returns False if no conjugation (also if empty) else True"
    if sTense == ":Y" or _dPatternConj[sTense][tTags[_dTenseIdx[sTense]]].get(sWho, False):
        return True
    return False


def _modifyStringWithSuffixCode (sWord, sSfx):
    "returns sWord modified by sSfx"
    if not sSfx:
        return ""
    if sSfx == "0":
        return sWord
    try:
        return sWord[:-(ord(sSfx[0])-48)] + sSfx[1:]  if sSfx[0] != '0'  else  sWord + sSfx[1:]  # 48 is the ASCII code for "0"
    except (IndexError, TypeError):
        return "## erreur, code : " + str(sSfx) + " ##"



class Verb ():
    "Verb and its conjugation"

    def __init__ (self, sVerb, sVerbPattern=""):
        # conjugate a unknown verb with rules from sVerbPattern
        if not isinstance(sVerb, str):
            raise TypeError("sVerb should be a string")
        if not sVerb:
            raise ValueError("Empty string.")

        if sVerbPattern == "":
            sVerbPattern = sVerb

        self.sVerb = sVerb
        self.sVerbAux = ""
        self._sRawInfo = getVtyp(sVerbPattern)
        self.sInfo = self._readableInfo()
        self.bProWithEn = (self._sRawInfo[5] == "e")
        self._tTags = _getTags(sVerbPattern)
        if not self._tTags:
            raise ValueError("Unknown verb.")
        self._tTagsAux = _getTags(self.sVerbAux)
        self.cGroup = self._sRawInfo[0]
        self.bUncomplete = self._sRawInfo.endswith("zz")
        self.sProLabel = "pronominal"
        if self._sRawInfo[5] == "_":
            self.nPronominable = -1
        elif self._sRawInfo[5] in ["q", "u", "v", "e"]:
            self.nPronominable = 0
        elif self._sRawInfo[5] == "p" or self._sRawInfo[5] == "r":
            self.nPronominable = 1
        elif self._sRawInfo[5] == "x":
            self.sProLabel = "cas particuliers"
            self.nPronominable = 2
        else:
            self.sProLabel = "# erreur #"
            self.nPronominable = -1
        self.dConj = {
            ":Y": {
                "label": "Infinitif",
                ":Y": sVerb,
            },
            ":P": {
                "label": "Participe présent",
                ":P": _getConjWithTags(sVerb, self._tTags, ":P", ":P"),
            },
            ":Q": {
                "label": "Participes passés",
                ":m:s": _getConjWithTags(sVerb, self._tTags, ":Q", ":m:s"),
                ":f:s": _getConjWithTags(sVerb, self._tTags, ":Q", ":f:s"),
                ":m:p": _getConjWithTags(sVerb, self._tTags, ":Q", ":m:p"),
                ":f:p": _getConjWithTags(sVerb, self._tTags, ":Q", ":f:p"),
            },
            ":Ip": {
                "label": "Présent",
                ":1s": _getConjWithTags(sVerb, self._tTags, ":Ip", ":1s"),
                ":1ś": _getConjWithTags(sVerb, self._tTags, ":Ip", ":1ś"),
                ":2s": _getConjWithTags(sVerb, self._tTags, ":Ip", ":2s"),
                ":3s": _getConjWithTags(sVerb, self._tTags, ":Ip", ":3s"),
                ":1p": _getConjWithTags(sVerb, self._tTags, ":Ip", ":1p"),
                ":2p": _getConjWithTags(sVerb, self._tTags, ":Ip", ":2p"),
                ":3p": _getConjWithTags(sVerb, self._tTags, ":Ip", ":3p"),
            },
            ":Iq": {
                "label": "Imparfait",
                ":1s": _getConjWithTags(sVerb, self._tTags, ":Iq", ":1s"),
                ":2s": _getConjWithTags(sVerb, self._tTags, ":Iq", ":2s"),
                ":3s": _getConjWithTags(sVerb, self._tTags, ":Iq", ":3s"),
                ":1p": _getConjWithTags(sVerb, self._tTags, ":Iq", ":1p"),
                ":2p": _getConjWithTags(sVerb, self._tTags, ":Iq", ":2p"),
                ":3p": _getConjWithTags(sVerb, self._tTags, ":Iq", ":3p"),
            },
            ":Is": {
                "label": "Passé simple",
                ":1s": _getConjWithTags(sVerb, self._tTags, ":Is", ":1s"),
                ":2s": _getConjWithTags(sVerb, self._tTags, ":Is", ":2s"),
                ":3s": _getConjWithTags(sVerb, self._tTags, ":Is", ":3s"),
                ":1p": _getConjWithTags(sVerb, self._tTags, ":Is", ":1p"),
                ":2p": _getConjWithTags(sVerb, self._tTags, ":Is", ":2p"),
                ":3p": _getConjWithTags(sVerb, self._tTags, ":Is", ":3p"),
            },
            ":If": {
                "label": "Futur",
                ":1s": _getConjWithTags(sVerb, self._tTags, ":If", ":1s"),
                ":2s": _getConjWithTags(sVerb, self._tTags, ":If", ":2s"),
                ":3s": _getConjWithTags(sVerb, self._tTags, ":If", ":3s"),
                ":1p": _getConjWithTags(sVerb, self._tTags, ":If", ":1p"),
                ":2p": _getConjWithTags(sVerb, self._tTags, ":If", ":2p"),
                ":3p": _getConjWithTags(sVerb, self._tTags, ":If", ":3p"),
            },
            ":Sp": {
                "label": "Présent subjonctif",
                ":1s": _getConjWithTags(sVerb, self._tTags, ":Sp", ":1s"),
                ":1ś": _getConjWithTags(sVerb, self._tTags, ":Sp", ":1ś"),
                ":2s": _getConjWithTags(sVerb, self._tTags, ":Sp", ":2s"),
                ":3s": _getConjWithTags(sVerb, self._tTags, ":Sp", ":3s"),
                ":1p": _getConjWithTags(sVerb, self._tTags, ":Sp", ":1p"),
                ":2p": _getConjWithTags(sVerb, self._tTags, ":Sp", ":2p"),
                ":3p": _getConjWithTags(sVerb, self._tTags, ":Sp", ":3p"),
            },
            ":Sq": {
                "label": "Imparfait subjonctif",
                ":1s": _getConjWithTags(sVerb, self._tTags, ":Sq", ":1s"),
                ":1ś": _getConjWithTags(sVerb, self._tTags, ":Sq", ":1ś"),
                ":2s": _getConjWithTags(sVerb, self._tTags, ":Sq", ":2s"),
                ":3s": _getConjWithTags(sVerb, self._tTags, ":Sq", ":3s"),
                ":1p": _getConjWithTags(sVerb, self._tTags, ":Sq", ":1p"),
                ":2p": _getConjWithTags(sVerb, self._tTags, ":Sq", ":2p"),
                ":3p": _getConjWithTags(sVerb, self._tTags, ":Sq", ":3p"),
            },
            ":K": {
                "label": "Conditionnel",
                ":1s": _getConjWithTags(sVerb, self._tTags, ":K", ":1s"),
                ":2s": _getConjWithTags(sVerb, self._tTags, ":K", ":2s"),
                ":3s": _getConjWithTags(sVerb, self._tTags, ":K", ":3s"),
                ":1p": _getConjWithTags(sVerb, self._tTags, ":K", ":1p"),
                ":2p": _getConjWithTags(sVerb, self._tTags, ":K", ":2p"),
                ":3p": _getConjWithTags(sVerb, self._tTags, ":K", ":3p"),
            },
            ":E": {
                "label": "Impératif",
                ":2s": _getConjWithTags(sVerb, self._tTags, ":E", ":2s"),
                ":1p": _getConjWithTags(sVerb, self._tTags, ":E", ":1p"),
                ":2p": _getConjWithTags(sVerb, self._tTags, ":E", ":2p"),
            },
        }

    def _readableInfo (self):
        "returns readable infos about sVerb"
        try:
            if not self._sRawInfo:
                return "verbe inconnu"
            if self._sRawInfo[7:8] == "e":
                self.sVerbAux = "être"
            else:
                self.sVerbAux = "avoir"
            sGroup = _dGroup.get(self._sRawInfo[0], "# erreur ")
            sInfo = ""
            if self._sRawInfo[3:4] == "t":
                sInfo = "transitif"
            elif self._sRawInfo[4:5] == "n":
                sInfo = "transitif indirect"
            elif self._sRawInfo[2:3] == "i":
                sInfo = "intransitif"
            elif self._sRawInfo[5:6] == "r":
                sInfo = "pronominal réciproque"
            elif self._sRawInfo[5:6] == "p":
                sInfo = "pronominal"
            if self._sRawInfo[5:6] in ["q", "u", "v", "e"]:
                sInfo = sInfo + " (+ usage pronominal)"
            if self._sRawInfo[6:7] == "m":
                sInfo = sInfo + " impersonnel"
            if not sInfo:
                sInfo = "# erreur - code : " + self._sRawInfo
            return sGroup + " · " + sInfo
        except (IndexError, TypeError):
            traceback.print_exc()
            return "# erreur"

    def infinitif (self, bPro, bNeg, bTpsCo, bInt, bFem):
        "returns string (conjugaison à l’infinitif)"
        try:
            if bTpsCo:
                sInfi = self.sVerbAux  if not bPro  else  "être"
            else:
                sInfi = self.sVerb
            if bPro:
                if self.bProWithEn:
                    sInfi = "s’en " + sInfi
                else:
                    sInfi = "s’" + sInfi  if _zStartVoy.search(sInfi)  else  "se " + sInfi
            if bNeg:
                sInfi = "ne pas " + sInfi
            if bTpsCo:
                sInfi += " " + self._seekPpas(bPro, bFem, self._sRawInfo[5] == "r")
            if bInt:
                sInfi += " … ?"
            return sInfi
        except (TypeError, IndexError):
            traceback.print_exc()
            return "# erreur"

    def participePasse (self, sWho):
        "returns past participle according to <sWho>"
        try:
            return self.dConj[":Q"][sWho]
        except KeyError:
            traceback.print_exc()
            return "# erreur"

    def participePresent (self, bPro, bNeg, bTpsCo, bInt, bFem):
        "returns string (conjugaison du participe présent)"
        try:
            if not self.dConj[":P"][":P"]:
                return ""
            if bTpsCo:
                sPartPre = _getConjWithTags(self.sVerbAux, self._tTagsAux, ":P", ":P")  if not bPro  else  getConj("être", ":P", ":P")
            else:
                sPartPre = self.dConj[":P"][":P"]
            if not sPartPre:
                return ""
            bEli = bool(_zStartVoy.search(sPartPre))
            if bPro:
                if self.bProWithEn:
                    sPartPre = "s’en " + sPartPre
                else:
                    sPartPre = "s’" + sPartPre  if bEli  else  "se " + sPartPre
            if bNeg:
                if bEli and not bPro:
                    sPartPre = "n’" + sPartPre + " pas"
                else:
                    sPartPre = "ne " + sPartPre + " pas"
            if bTpsCo:
                sPartPre += " " + self._seekPpas(bPro, bFem, self._sRawInfo[5] == "r")
            if bInt:
                sPartPre += " … ?"
            return sPartPre
        except (KeyError, TypeError, IndexError):
            traceback.print_exc()
            return "# erreur"

    def conjugue (self, sTemps, sWho, bPro, bNeg, bTpsCo, bInt, bFem):
        "returns string (conjugue le verbe au temps <sTemps> pour <sWho>) "
        try:
            if not self.dConj[sTemps][sWho]:
                return ""
            if not bTpsCo and bInt and sWho == ":1s" and self.dConj[sTemps].get(":1ś", False):
                sWho = ":1ś"
            if bTpsCo:
                sConj = _getConjWithTags(self.sVerbAux, self._tTagsAux, sTemps, sWho)  if not bPro  else  getConj("être", sTemps, sWho)
            else:
                sConj = self.dConj[sTemps][sWho]
            if not sConj:
                return ""
            bEli = bool(_zStartVoy.search(sConj))
            if bPro:
                if not self.bProWithEn:
                    sConj = _dProObjEl[sWho] + sConj  if bEli  else _dProObj[sWho] + sConj
                else:
                    sConj = _dProObjEl[sWho] + "en " + sConj
            if bNeg:
                sConj = "n’" + sConj  if bEli and not bPro  else  "ne " + sConj
            if bInt:
                if sWho == ":3s" and not _zNeedTeuph.search(sConj):
                    sConj += "-t"
                sConj += "-" + self._getPronomSujet(sWho, bFem)
            else:
                if sWho == ":1s" and bEli and not bNeg and not bPro:
                    sConj = "j’" + sConj
                else:
                    sConj = self._getPronomSujet(sWho, bFem) + " " + sConj
            if bNeg:
                sConj += " pas"
            if bTpsCo:
                sConj += " " + self._seekPpas(bPro, bFem, sWho.endswith("p") or self._sRawInfo[5] == "r")
            if bInt:
                sConj += " … ?"
            return sConj
        except (KeyError, TypeError, IndexError):
            traceback.print_exc()
            return "# erreur"

    def _getPronomSujet (self, sWho, bFem):
        try:
            if sWho == ":3s":
                if self._sRawInfo[5] == "r":
                    return "on"
                if bFem:
                    return "elle"
            if sWho == ":3p" and bFem:
                return "elles"
            return _dProSuj[sWho]
        except (KeyError, IndexError):
            traceback.print_exc()
            return "# erreur"

    def imperatif (self, sWho, bPro, bNeg, bTpsCo, bFem):
        "returns string (conjugaison à l’impératif)"
        try:
            if not self.dConj[":E"][sWho]:
                return ""
            if bTpsCo:
                sImpe = _getConjWithTags(self.sVerbAux, self._tTagsAux, ":E", sWho)  if not bPro  else  getConj(u"être", ":E", sWho)
            else:
                sImpe = self.dConj[":E"][sWho]
            if not sImpe:
                return ""
            bEli = bool(_zStartVoy.search(sImpe))
            if bNeg:
                if bPro:
                    if not self.bProWithEn:
                        if bEli and sWho == ":2s":
                            sImpe = "ne t’" + sImpe + " pas"
                        else:
                            sImpe = _dImpeProNeg[sWho] + sImpe + " pas"
                    else:
                        sImpe = _dImpeProNegEn[sWho] + sImpe + " pas"
                else:
                    sImpe = "n’" + sImpe + " pas"  if bEli  else  "ne " + sImpe + " pas"
            elif bPro:
                sImpe = sImpe + _dImpeProEn[sWho]  if self.bProWithEn  else  sImpe + _dImpePro[sWho]
            if bTpsCo:
                return sImpe + " " + self._seekPpas(bPro, bFem, sWho.endswith("p") or self._sRawInfo[5] == "r")
            return sImpe
        except (KeyError, TypeError, IndexError):
            traceback.print_exc()
            return "# erreur"

    def _seekPpas (self, bPro, bFem, bPlur):
        try:
            if not bPro and self.sVerbAux == "avoir":
                return self.dConj[":Q"][":m:s"]
            if not bFem:
                return self.dConj[":Q"][":f:s"]  if bPlur and self.dConj[":Q"][":f:s"]  else  self.dConj[":Q"][":m:s"]
            if not bPlur:
                return self.dConj[":Q"][":m:p"]  if self.dConj[":Q"][":m:p"]  else  self.dConj[":Q"][":m:s"]
            return self.dConj[":Q"][":f:p"]  if self.dConj[":Q"][":f:p"]  else  self.dConj[":Q"][":m:s"]
        except KeyError:
            traceback.print_exc()
            return "# erreur"

    def createConjTable (self, bPro=False, bNeg=False, bTpsCo=False, bInt=False, bFem=False):
        "return a dictionary of all conjugations with titles, according to options (used to be displayed as is)"
        dConjTable = {
            "t_infi":   "Infinitif",
            "infi":     self.infinitif(bPro, bNeg, bTpsCo, bInt, bFem),
            "t_ppre":   "Participe présent",
            "ppre":     self.participePresent(bPro, bNeg, bTpsCo, bInt, bFem),
            "t_ppas":   "Participes passés",
            "ppas1":    self.participePasse(":m:s"),
            "ppas2":    self.participePasse(":f:s"),
            "ppas3":    self.participePasse(":m:p"),
            "ppas4":    self.participePasse(":f:p"),
            "t_imp":    "Impératif",
            "t_impe":   ""  if bInt  else "Présent"  if not bTpsCo  else "Passé",
            "impe1":    self.imperatif(":2s", bPro, bNeg, bTpsCo, bFem)  if not bInt  else "",
            "impe2":    self.imperatif(":1p", bPro, bNeg, bTpsCo, bFem)  if not bInt  else "",
            "impe3":    self.imperatif(":2p", bPro, bNeg, bTpsCo, bFem)  if not bInt  else "",
            "t_indi":   "Indicatif",
            "t_ipre":   "Présent"      if not bTpsCo  else "Passé composé",
            "ipre1":    self.conjugue(":Ip", ":1s", bPro, bNeg, bTpsCo, bInt, bFem),
            "ipre2":    self.conjugue(":Ip", ":2s", bPro, bNeg, bTpsCo, bInt, bFem),
            "ipre3":    self.conjugue(":Ip", ":3s", bPro, bNeg, bTpsCo, bInt, bFem),
            "ipre4":    self.conjugue(":Ip", ":1p", bPro, bNeg, bTpsCo, bInt, bFem),
            "ipre5":    self.conjugue(":Ip", ":2p", bPro, bNeg, bTpsCo, bInt, bFem),
            "ipre6":    self.conjugue(":Ip", ":3p", bPro, bNeg, bTpsCo, bInt, bFem),
            "t_iimp":   "Imparfait"    if not bTpsCo  else "Plus-que-parfait",
            "iimp1":    self.conjugue(":Iq", ":1s", bPro, bNeg, bTpsCo, bInt, bFem),
            "iimp2":    self.conjugue(":Iq", ":2s", bPro, bNeg, bTpsCo, bInt, bFem),
            "iimp3":    self.conjugue(":Iq", ":3s", bPro, bNeg, bTpsCo, bInt, bFem),
            "iimp4":    self.conjugue(":Iq", ":1p", bPro, bNeg, bTpsCo, bInt, bFem),
            "iimp5":    self.conjugue(":Iq", ":2p", bPro, bNeg, bTpsCo, bInt, bFem),
            "iimp6":    self.conjugue(":Iq", ":3p", bPro, bNeg, bTpsCo, bInt, bFem),
            "t_ipsi":   "Passé simple" if not bTpsCo  else "Passé antérieur",
            "ipsi1":    self.conjugue(":Is", ":1s", bPro, bNeg, bTpsCo, bInt, bFem),
            "ipsi2":    self.conjugue(":Is", ":2s", bPro, bNeg, bTpsCo, bInt, bFem),
            "ipsi3":    self.conjugue(":Is", ":3s", bPro, bNeg, bTpsCo, bInt, bFem),
            "ipsi4":    self.conjugue(":Is", ":1p", bPro, bNeg, bTpsCo, bInt, bFem),
            "ipsi5":    self.conjugue(":Is", ":2p", bPro, bNeg, bTpsCo, bInt, bFem),
            "ipsi6":    self.conjugue(":Is", ":3p", bPro, bNeg, bTpsCo, bInt, bFem),
            "t_ifut":   "Futur"        if not bTpsCo  else "Futur antérieur",
            "ifut1":    self.conjugue(":If", ":1s", bPro, bNeg, bTpsCo, bInt, bFem),
            "ifut2":    self.conjugue(":If", ":2s", bPro, bNeg, bTpsCo, bInt, bFem),
            "ifut3":    self.conjugue(":If", ":3s", bPro, bNeg, bTpsCo, bInt, bFem),
            "ifut4":    self.conjugue(":If", ":1p", bPro, bNeg, bTpsCo, bInt, bFem),
            "ifut5":    self.conjugue(":If", ":2p", bPro, bNeg, bTpsCo, bInt, bFem),
            "ifut6":    self.conjugue(":If", ":3p", bPro, bNeg, bTpsCo, bInt, bFem),
            "t_cond":   "Conditionnel",
            "t_conda":  "Présent"      if not bTpsCo  else "Passé (1ʳᵉ forme)",
            "conda1":   self.conjugue(":K", ":1s", bPro, bNeg, bTpsCo, bInt, bFem),
            "conda2":   self.conjugue(":K", ":2s", bPro, bNeg, bTpsCo, bInt, bFem),
            "conda3":   self.conjugue(":K", ":3s", bPro, bNeg, bTpsCo, bInt, bFem),
            "conda4":   self.conjugue(":K", ":1p", bPro, bNeg, bTpsCo, bInt, bFem),
            "conda5":   self.conjugue(":K", ":2p", bPro, bNeg, bTpsCo, bInt, bFem),
            "conda6":   self.conjugue(":K", ":3p", bPro, bNeg, bTpsCo, bInt, bFem),
            "t_condb":  ""             if not bTpsCo  else "Passé (2ᵉ forme)",
            "condb1":   self.conjugue(":Sq", ":1s", bPro, bNeg, bTpsCo, bInt, bFem)  if bTpsCo  else "",
            "condb2":   self.conjugue(":Sq", ":2s", bPro, bNeg, bTpsCo, bInt, bFem)  if bTpsCo  else "",
            "condb3":   self.conjugue(":Sq", ":3s", bPro, bNeg, bTpsCo, bInt, bFem)  if bTpsCo  else "",
            "condb4":   self.conjugue(":Sq", ":1p", bPro, bNeg, bTpsCo, bInt, bFem)  if bTpsCo  else "",
            "condb5":   self.conjugue(":Sq", ":2p", bPro, bNeg, bTpsCo, bInt, bFem)  if bTpsCo  else "",
            "condb6":   self.conjugue(":Sq", ":3p", bPro, bNeg, bTpsCo, bInt, bFem)  if bTpsCo  else "",
            "t_subj":   "Subjonctif",
            "t_spre":   ""  if bInt  else "Présent"      if not bTpsCo  else "Passé",
            "spre1":    self.conjugue(":Sp", ":1s", bPro, bNeg, bTpsCo, bInt, bFem)  if not bInt  else "",
            "spre2":    self.conjugue(":Sp", ":2s", bPro, bNeg, bTpsCo, bInt, bFem)  if not bInt  else "",
            "spre3":    self.conjugue(":Sp", ":3s", bPro, bNeg, bTpsCo, bInt, bFem)  if not bInt  else "",
            "spre4":    self.conjugue(":Sp", ":1p", bPro, bNeg, bTpsCo, bInt, bFem)  if not bInt  else "",
            "spre5":    self.conjugue(":Sp", ":2p", bPro, bNeg, bTpsCo, bInt, bFem)  if not bInt  else "",
            "spre6":    self.conjugue(":Sp", ":3p", bPro, bNeg, bTpsCo, bInt, bFem)  if not bInt  else "",
            "t_simp":   ""  if bInt  else "Imparfait"    if not bTpsCo  else "Plus-que-parfait",
            "simp1":    self.conjugue(":Sq", ":1s", bPro, bNeg, bTpsCo, bInt, bFem)  if not bInt  else "",
            "simp2":    self.conjugue(":Sq", ":2s", bPro, bNeg, bTpsCo, bInt, bFem)  if not bInt  else "",
            "simp3":    self.conjugue(":Sq", ":3s", bPro, bNeg, bTpsCo, bInt, bFem)  if not bInt  else "",
            "simp4":    self.conjugue(":Sq", ":1p", bPro, bNeg, bTpsCo, bInt, bFem)  if not bInt  else "",
            "simp5":    self.conjugue(":Sq", ":2p", bPro, bNeg, bTpsCo, bInt, bFem)  if not bInt  else "",
            "simp6":    self.conjugue(":Sq", ":3p", bPro, bNeg, bTpsCo, bInt, bFem)  if not bInt  else ""
        }
        return dConjTable
