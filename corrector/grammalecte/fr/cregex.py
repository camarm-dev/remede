"""
Grammalecte - Compiled regular expressions
"""

import re

#### Lemme
Lemma = re.compile(r"^>(\w[\w-]*)")

#### Analyses
GenderNumber = re.compile(":[mfe]:[spi]")

#### Nom et adjectif
NA = re.compile(":[NA]")

## nombre
NAs = re.compile(":[NA].*:s")
NAp = re.compile(":[NA].*:p")
NAi = re.compile(":[NA].*:i")
NAsi = re.compile(":[NA].*:[si]")
NApi = re.compile(":[NA].*:[pi]")

## genre
NAm = re.compile(":[NA].*:m")
NAf = re.compile(":[NA].*:f")
NAe = re.compile(":[NA].*:e")
NAme = re.compile(":[NA].*:[me]")
NAfe = re.compile(":[NA].*:[fe]")

## nombre et genre
# singuilier
NAms = re.compile(":[NA].*:m.*:s")
NAfs = re.compile(":[NA].*:f.*:s")
NAes = re.compile(":[NA].*:e.*:s")
NAmes = re.compile(":[NA].*:[me].*:s")
NAfes = re.compile(":[NA].*:[fe].*:s")

# singulier et invariable
NAmsi = re.compile(":[NA].*:m.*:[si]")
NAfsi = re.compile(":[NA].*:f.*:[si]")
NAesi = re.compile(":[NA].*:e.*:[si]")
NAmesi = re.compile(":[NA].*:[me].*:[si]")
NAfesi = re.compile(":[NA].*:[fe].*:[si]")

# pluriel
NAmp = re.compile(":[NA].*:m.*:p")
NAfp = re.compile(":[NA].*:f.*:p")
NAep = re.compile(":[NA].*:e.*:p")
NAmep = re.compile(":[NA].*:[me].*:p")
NAfep = re.compile(":[NA].*:[me].*:p")

# pluriel et invariable
NAmpi = re.compile(":[NA].*:m.*:[pi]")
NAfpi = re.compile(":[NA].*:f.*:[pi]")
NAepi = re.compile(":[NA].*:e.*:[pi]")
NAmepi = re.compile(":[NA].*:[me].*:[pi]")
NAfepi = re.compile(":[NA].*:[fe].*:[pi]")

# divers
AD = re.compile(":[AB]")

#### Verbe
Vconj = re.compile(":[123][sp]")
Vconj123 = re.compile(":V[123].*:[123][sp]")

#### Nom | Adjectif | Verbe
NVconj = re.compile(":(?:N|[123][sp])")
NAVconj = re.compile(":(?:N|A|[123][sp])")

#### Spécifique
NnotA = re.compile(":N(?!:A)")
PNnotA = re.compile(":(?:N(?!:A)|Q)")

#### Noms propres
NP = re.compile(":(?:M[12P]|T)")
NPm = re.compile(":(?:M[12P]|T):m")
NPf = re.compile(":(?:M[12P]|T):f")
NPe = re.compile(":(?:M[12P]|T):e")


#### FONCTIONS

def getLemmaOfMorph (s):
    "return lemma in morphology <s>"
    return Lemma.search(s).group(1)

def agreement (l1, l2):
    "returns True if agreement in gender and number is possible between morphologies <l1> and <l2>"
    sGender1, sNumber1 = getGenderNumber(l1)
    sGender2, sNumber2 = getGenderNumber(l2)
    if sNumber1 != ":i" and sNumber2 != ":i" and sNumber1 != sNumber2:
        return False
    if sGender1 != ":e" and sGender2 != ":e" and sGender1 != sGender2:
        return False
    return True

def checkConjVerb (lMorph, sReqConj):
    "returns True if <sReqConj> in <lMorph>"
    return any(sReqConj in s  for s in lMorph)

def getGenderNumber (lMorph):
    "returns tuple (gender, number) of word: (':m', ':f', ':e' or empty string) and (':s', ':p', ':i' or empty string)"
    sGender = ""
    sNumber = ""
    for sMorph in lMorph:
        m = GenderNumber.search(sMorph)
        if m:
            sGenderx = m.group(0)[0:2]
            sNumberx = m.group(0)[2:4]
            if not sGender:
                sGender = sGenderx
            elif sGender != sGenderx:
                sGender = ":e"
            if not sNumber:
                sNumber = sNumberx
            elif sNumber != sNumberx:
                sNumber = ":i"
    return sGender, sNumber


# NOTE :  isWhat (lMorph)    returns True   if lMorph contains nothing else than What
#         mbWhat (lMorph)    returns True   if lMorph contains What at least once

## isXXX = it’s certain

def isNom (lMorph):
    "returns True if all morphologies are “nom”"
    return all(":N" in s  for s in lMorph)

def isNomNotAdj (lMorph):
    "returns True if all morphologies are “nom”, but not “adjectif”"
    return all(NnotA.search(s)  for s in lMorph)

def isAdj (lMorph):
    "returns True if all morphologies are “adjectif”"
    return all(":A" in s  for s in lMorph)

def isNomAdj (lMorph):
    "returns True if all morphologies are “nom” or “adjectif”"
    return all(NA.search(s)  for s in lMorph)

def isNomVconj (lMorph):
    "returns True if all morphologies are “nom” or “verbe conjugué”"
    return all(NVconj.search(s)  for s in lMorph)

def isInv (lMorph):
    "returns True if all morphologies are “invariable”"
    return all(":i" in s  for s in lMorph)

def isSg (lMorph):
    "returns True if all morphologies are “singulier”"
    return all(":s" in s  for s in lMorph)

def isPl (lMorph):
    "returns True if all morphologies are “pluriel”"
    return all(":p" in s  for s in lMorph)

def isEpi (lMorph):
    "returns True if all morphologies are “épicène”"
    return all(":e" in s  for s in lMorph)

def isMas (lMorph):
    "returns True if all morphologies are “masculin”"
    return all(":m" in s  for s in lMorph)

def isFem (lMorph):
    "returns True if all morphologies are “féminin”"
    return all(":f" in s  for s in lMorph)


## mbXXX = MAYBE XXX

def mbNom (lMorph):
    "returns True if one morphology is “nom”"
    return any(":N" in s  for s in lMorph)

def mbAdj (lMorph):
    "returns True if one morphology is “adjectif”"
    return any(":A" in s  for s in lMorph)

def mbAdjNb (lMorph):
    "returns True if one morphology is “adjectif” or “nombre”"
    return any(AD.search(s)  for s in lMorph)

def mbNomAdj (lMorph):
    "returns True if one morphology is “nom” or “adjectif”"
    return any(NA.search(s)  for s in lMorph)

def mbNomNotAdj (lMorph):
    "returns True if one morphology is “nom”, but not “adjectif”"
    bResult = False
    for s in lMorph:
        if ":A" in s:
            return False
        if ":N" in s:
            bResult = True
    return bResult

def mbPpasNomNotAdj (lMorph):
    "returns True if one morphology is “nom” or “participe passé”, but not “adjectif”"
    return any(PNnotA.search(s)  for s in lMorph)

def mbVconj (lMorph):
    "returns True if one morphology is “nom” or “verbe conjugué”"
    return any(Vconj.search(s)  for s in lMorph)

def mbVconj123 (lMorph):
    "returns True if one morphology is “nom” or “verbe conjugué” (but not “avoir” or “être”)"
    return any(Vconj123.search(s)  for s in lMorph)

def mbMG (lMorph):
    "returns True if one morphology is “mot grammatical”"
    return any(":G" in s  for s in lMorph)

def mbInv (lMorph):
    "returns True if one morphology is “invariable”"
    return any(":i" in s  for s in lMorph)

def mbSg (lMorph):
    "returns True if one morphology is “singulier”"
    return any(":s" in s  for s in lMorph)

def mbPl (lMorph):
    "returns True if one morphology is “pluriel”"
    return any(":p" in s  for s in lMorph)

def mbEpi (lMorph):
    "returns True if one morphology is “épicène”"
    return any(":e" in s  for s in lMorph)

def mbMas (lMorph):
    "returns True if one morphology is “masculin”"
    return any(":m" in s  for s in lMorph)

def mbFem (lMorph):
    "returns True if one morphology is “féminin”"
    return any(":f" in s  for s in lMorph)

def mbNpr (lMorph):
    "returns True if one morphology is “nom propre” or “titre de civilité”"
    return any(NP.search(s)  for s in lMorph)

def mbNprMasNotFem (lMorph):
    "returns True if one morphology is “nom propre masculin” but not “féminin”"
    if any(NPf.search(s)  for s in lMorph):
        return False
    return any(NPm.search(s)  for s in lMorph)
