"""
Grammalecte - Suggestion phonétique
"""

# License: GPL 3

import re

from .phonet_data import dWord as _dWord
from .phonet_data import lSet as _lSet
from .phonet_data import dMorph as _dMorph


def hasSimil (sWord, sPattern=None):
    "return True if there is list of words phonetically similar to <sWord>"
    if not sWord:
        return False
    if sWord in _dWord:
        if sPattern:
            return any(re.search(sPattern, sMorph)  for sSimil in getSimil(sWord)  for sMorph in _dMorph.get(sSimil, []))
        return True
    if sWord[0:1].isupper():
        sWord = sWord.lower()
        if sWord in _dWord:
            if sPattern:
                return any(re.search(sPattern, sMorph)  for sSimil in getSimil(sWord)  for sMorph in _dMorph.get(sSimil, []))
            return True
    return False


def getSimil (sWord):
    "return list of words phonetically similar to <sWord>"
    if not sWord:
        return []
    if sWord in _dWord:
        return _lSet[_dWord[sWord]]
    if sWord[0:1].isupper():
        sWord = sWord.lower()
        if sWord in _dWord:
            return _lSet[_dWord[sWord]]
    return []


def selectSimil (sWord, sPattern):
    "return a list of words phonetically similar to <sWord> and whom POS is matching <sPattern>"
    if not sPattern:
        return getSimil(sWord)
    aSelect = []
    for sSimil in getSimil(sWord):
        for sMorph in _dMorph.get(sSimil, []):
            if re.search(sPattern, sMorph):
                aSelect.append(sSimil)
    return aSelect


def _getSetNumber (sWord):
    "return the set number where <sWord> belongs, else -1"
    if sWord in _dWord:
        return _dWord[sWord]
    if sWord[0:1].isupper():
        if sWord.lower() in _dWord:
            return _dWord[sWord.lower()]
        if sWord.isupper() and sWord.capitalize() in _dWord:
            return _dWord[sWord.capitalize()]
    return -1


def isSimilAs (sWord, sSimil):
    "return True if <sWord> phonetically similar to <sSimil> (<sWord> tested with several casing)"
    if not sWord or not sSimil:
        return False
    n = _getSetNumber(sWord)
    if n == -1:
        return False
    return n == _getSetNumber(sSimil)
