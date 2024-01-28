"""
Operations on strings:
- calculate distance between two strings
- transform strings with transformation codes
"""

import unicodedata
import re

from .char_player import distanceBetweenChars, dDistanceBetweenChars


#### N-GRAMS

def getNgrams (sWord, n=2):
    "return a list of Ngrams strings"
    return [ sWord[i:i+n]  for i in range(len(sWord)-n+1) ]



#### WORD NORMALIZATION

_xTransCharsForSpelling = str.maketrans({
    'ſ': 's',  'ﬃ': 'ffi',  'ﬄ': 'ffl',  'ﬀ': 'ff',  'ﬅ': 'ft',  'ﬁ': 'fi',  'ﬂ': 'fl',  'ﬆ': 'st',
    "'": '’'
})

def spellingNormalization (sWord):
    "nomalization NFC and removing ligatures"
    return unicodedata.normalize("NFC", sWord.translate(_xTransCharsForSpelling))


_xTransCharsForSimplification = str.maketrans({
    'à': 'a',  'é': 'é',  'î': 'i',  'ô': 'o',  'û': 'u',  'ÿ': 'y',
    'â': 'a',  'è': 'é',  'ï': 'i',  'ö': 'o',  'ù': 'u',  'ŷ': 'y',
    'ä': 'a',  'ê': 'é',  'í': 'i',  'ó': 'o',  'ü': 'u',  'ý': 'y',
    'á': 'a',  'ë': 'é',  'ì': 'i',  'ò': 'o',  'ú': 'u',  'ỳ': 'y',
    'ā': 'a',  'ē': 'é',  'ī': 'i',  'ō': 'o',  'ū': 'u',  'ȳ': 'y',
    'ç': 'c',  'ñ': 'n',
    'œ': 'oe',  'æ': 'ae',
    'ſ': 's',  'ﬃ': 'ffi',  'ﬄ': 'ffl',  'ﬀ': 'ff',  'ﬅ': 'ft',  'ﬁ': 'fi',  'ﬂ': 'fl',  'ﬆ': 'st',
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
    "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9",
    "’": "", "'": "", "ʼ": "", "‘": "", "‛": "", "´": "", "`": "", "′": "", "‵": "", "՚": "", "ꞌ": "", "Ꞌ": "",
    "-": ""
})

def simplifyWord (sWord):
    "word simplication before calculating distance between words"
    sWord = sWord.lower().translate(_xTransCharsForSimplification)
    sNewWord = ""
    for i, c in enumerate(sWord, 1):
        if c != sWord[i:i+1] or (c == 'e' and sWord[i:i+2] != "ee"):  # exception for <e> to avoid confusion between crée / créai
            sNewWord += c
    return sNewWord.replace("eau", "o").replace("au", "o").replace("ai", "éi").replace("ei", "é").replace("ph", "f")


def cleanWord (sWord):
    "remove letters repeated more than 2 times"
    return re.sub("(.)\\1{2,}", '\\1\\1', sWord)


_xTransNumbersToExponent = str.maketrans({
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"
})

def numbersToExponent (sWord):
    "convert numeral chars to exponant chars"
    return sWord.translate(_xTransNumbersToExponent)



#### DISTANCE CALCULATIONS

def longestCommonSubstring (s1, s2):
    "longest common substring"
    # http://en.wikipedia.org/wiki/Longest_common_substring_problem
    # http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Longest_common_substring
    lMatrix = [ [0]*(1+len(s2)) for i in range(1+len(s1)) ]
    nLongest, nLongestX = 0, 0
    for x in range(1, 1+len(s1)):
        for y in range(1, 1+len(s2)):
            if s1[x-1] == s2[y-1]:
                lMatrix[x][y] = lMatrix[x-1][y-1] + 1
                if lMatrix[x][y] > nLongest:
                    nLongest = lMatrix[x][y]
                    nLongestX = x
            else:
                lMatrix[x][y] = 0
    return s1[nLongestX-nLongest : nLongestX]


def distanceDamerauLevenshtein (s1, s2):
    "distance of Damerau-Levenshtein between <s1> and <s2>"
    # https://fr.wikipedia.org/wiki/Distance_de_Damerau-Levenshtein
    d = {}
    nLen1 = len(s1)
    nLen2 = len(s2)
    for i in range(-1, nLen1+1):
        d[i, -1] = i + 1
    for j in range(-1, nLen2+1):
        d[-1, j] = j + 1
    for i in range(nLen1):
        for j in range(nLen2):
            #nCost = 0  if s1[i] == s2[j]  else 1
            nCost = distanceBetweenChars(s1[i], s2[j])
            d[i, j] = min(
                d[i-1, j]   + 1,        # Deletion
                d[i,   j-1] + 1,        # Insertion
                d[i-1, j-1] + nCost,    # Substitution
            )
            if i and j and s1[i] == s2[j-1] and s1[i-1] == s2[j]:
                d[i, j] = min(d[i, j], d[i-2, j-2] + nCost)     # Transposition
    return d[nLen1-1, nLen2-1]


def distanceJaroWinkler (sWord1, sWord2, fBoost = .666):
    "distance of Jaro-Winkler between <sWord1> and <sWord2>, returns a float"
    # https://github.com/thsig/jaro-winkler-JS
    #if (sWord1 == sWord2): return 1.0
    nLen1 = len(sWord1)
    nLen2 = len(sWord2)
    nMax = max(nLen1, nLen2)
    aFlags1 = [ None for _ in range(nMax) ]
    aFlags2 = [ None for _ in range(nMax) ]
    nSearchRange = (max(nLen1, nLen2) // 2) - 1
    nMinLen = min(nLen1, nLen2)

    # Looking only within the search range, count and flag the matched pairs.
    nCommon = 0
    yl1 = nLen2 - 1
    for i in range(nLen1):
        nLowLim = i - nSearchRange  if i >= nSearchRange  else 0
        nHiLim  = i + nSearchRange  if (i + nSearchRange) <= yl1  else yl1
        for j in range(nLowLim, nHiLim+1):
            if aFlags2[j] != 1 and sWord1[j:j+1] == sWord2[i:i+1]:
                aFlags1[j] = 1
                aFlags2[i] = 1
                nCommon += 1
                break

    # Return if no characters in common
    if nCommon == 0:
        return 0.0

    # Count the number of transpositions
    k = 0
    nTrans = 0
    for i in range(nLen1):
        if aFlags1[i] == 1:
            for j in range(k, nLen2):
                if aFlags2[j] == 1:
                    k = j + 1
                    break
            if sWord1[i] != sWord2[j]:
                nTrans += 1
    nTrans = nTrans // 2

    # Adjust for similarities in nonmatched characters
    nSimi = 0
    if nMinLen > nCommon:
        for i in range(nLen1):
            if not aFlags1[i]:
                for j in range(nLen2):
                    if not aFlags2[j]:
                        if sWord1[i] in dDistanceBetweenChars and sWord2[j] in dDistanceBetweenChars[sWord1[i]]:
                            nSimi += dDistanceBetweenChars[sWord1[i]][sWord2[j]]
                            aFlags2[j] = 2
                            break

    fSim = (nSimi / 10.0) + nCommon

    # Main weight computation
    fWeight = fSim / nLen1 + fSim / nLen2 + (nCommon - nTrans) / nCommon
    fWeight = fWeight / 3

    # Continue to boost the weight if the strings are similar
    if fWeight > fBoost:
        # Adjust for having up to the first 4 characters in common
        j = 4  if nMinLen >= 4  else nMinLen
        i = 0
        while i < j  and sWord1[i] == sWord2[i]:
            i += 1
        if i:
            fWeight += i * 0.1 * (1.0 - fWeight)
        # Adjust for long strings.
        # After agreeing beginning chars, at least two more must agree
        # and the agreeing characters must be more than half of the
        # remaining characters.
        if nMinLen > 4  and  nCommon > i + 1  and  2 * nCommon >= nMinLen + i:
            fWeight += (1 - fWeight) * ((nCommon - i - 1) / (nLen1 * nLen2 - i*2 + 2))
    return fWeight


def distanceSift4 (s1, s2, nMaxOffset=5):
    "implementation of general Sift4."
    # https://siderite.blogspot.com/2014/11/super-fast-and-accurate-string-distance.html
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)
    nLen1, nLen2 = len(s1), len(s2)
    i1, i2 = 0, 0   # Cursors for each string
    nLargestCS = 0  # Largest common substring
    nLocalCS = 0    # Local common substring
    nTrans = 0      # Number of transpositions ('ab' vs 'ba')
    lOffset = []    # Offset pair array, for computing the transpositions

    while i1 < nLen1 and i2 < nLen2:
        if s1[i1] == s2[i2]:
            nLocalCS += 1
            # Check if current match is a transposition
            bTrans = False
            i = 0
            while i < len(lOffset):
                t = lOffset[i]
                if i1 <= t[0] or i2 <= t[1]:
                    bTrans = abs(i2-i1) >= abs(t[1] - t[0])
                    if bTrans:
                        nTrans += 1
                    elif not t[2]:
                        t[2] = True
                        nTrans += 1
                    break
                if i1 > t[1] and i2 > t[0]:
                    del lOffset[i]
                else:
                    i += 1
            lOffset.append([i1, i2, bTrans])
        else:
            nLargestCS += nLocalCS
            nLocalCS = 0
            if i1 != i2:
                i1 = i2 = min(i1, i2)
            for i in range(nMaxOffset):
                if i1 + i >= nLen1 and i2 + i >= nLen2:
                    break
                if i1 + i < nLen1 and s1[i1+i] == s2[i2]:
                    i1 += i - 1
                    i2 -= 1
                    break
                if i2 + i < nLen2 and s1[i1] == s2[i2+i]:
                    i2 += i - 1
                    i1 -= 1
                    break
        i1 += 1
        i2 += 1
        if i1 >= nLen1 or i2 >= nLen2:
            nLargestCS += nLocalCS
            nLocalCS = 0
            i1 = i2 = min(i1, i2)
    nLargestCS += nLocalCS
    return round(max(nLen1, nLen2) - nLargestCS + nTrans)


def showDistance (s1, s2):
    "display Damerau-Levenshtein distance and Sift4 distance between <s1> and <s2>"
    print("Jaro-Winkler: " + s1 + "/" + s2 + " = " + distanceJaroWinkler(s1, s2))
    print("Damerau-Levenshtein: " + s1 + "/" + s2 + " = " + distanceDamerauLevenshtein(s1, s2))
    print("Sift4:" + s1 + "/" + s2 + " = " + distanceSift4(s1, s2))




#### STEMMING OPERATIONS

## No stemming

def noStemming (sFlex, sStem):
    "return <sStem>"
    return sStem

def rebuildWord (sFlex, sCode1, sCode2):
    """ Change <sFlex> with codes (each inserts a char at a defined possition).
        <I forgot what purpose it has…>
    """
    if sCode1 == "_":
        return sFlex
    n, c = sCode1.split(":")
    sFlex = sFlex[:n] + c + sFlex[n:]
    if sCode2 == "_":
        return sFlex
    n, c = sCode2.split(":")
    return sFlex[:n] + c + sFlex[n:]


## Define affixes for stemming

# Note: 48 is the ASCII code for "0"


# Suffix only
def defineSuffixCode (sFlex, sStem):
    """ Returns a string defining how to get stem from flexion
            "n(sfx)"
        with n: a char with numeric meaning, "0" = 0, "1" = 1, ... ":" = 10, etc. (See ASCII table.) Says how many letters to strip from flexion.
             sfx [optional]: string to add on flexion
        Examples:
            "0": strips nothing, adds nothing
            "1er": strips 1 letter, adds "er"
            "2": strips 2 letters, adds nothing
    """
    if sFlex == sStem:
        return "0"
    jSfx = 0
    for i in range(min(len(sFlex), len(sStem))):
        if sFlex[i] != sStem[i]:
            break
        jSfx += 1
    return chr(len(sFlex)-jSfx+48) + sStem[jSfx:]


def changeWordWithSuffixCode (sWord, sSfxCode):
    "apply transformation code <sSfxCode> on <sWord> and return the result string"
    if sSfxCode == "0":
        return sWord
    return sWord[:-(ord(sSfxCode[0])-48)] + sSfxCode[1:]  if sSfxCode[0] != '0'  else sWord + sSfxCode[1:]


# Prefix and suffix

def defineAffixCode (sFlex, sStem):
    """ Returns a string defining how to get stem from flexion. Examples:
            "0" if stem = flexion
            "stem" if no common substring
            "n(pfx)/m(sfx)"
        with n and m: chars with numeric meaning, "0" = 0, "1" = 1, ... ":" = 10, etc. (See ASCII table.) Says how many letters to strip from flexion.
            pfx [optional]: string to add before the flexion
            sfx [optional]: string to add after the flexion
    """
    if sFlex == sStem:
        return "0"
    # is stem a substring of flexion?
    n = sFlex.find(sStem)
    if n >= 0:
        return "{}/{}".format(chr(n+48), chr(len(sFlex)-(len(sStem)+n)+48))
    # no, so we are looking for common substring
    sSubs = longestCommonSubstring(sFlex, sStem)
    if len(sSubs) > 1:
        iPos = sStem.find(sSubs)
        sPfx = sStem[:iPos]
        sSfx = sStem[iPos+len(sSubs):]
        n = sFlex.find(sSubs)
        m = len(sFlex) - (len(sSubs)+n)
        return chr(n+48) + sPfx + "/" + chr(m+48) + sSfx
    return sStem


def changeWordWithAffixCode (sWord, sAffCode):
    "apply transformation code <sAffCode> on <sWord> and return the result string"
    if sAffCode == "0":
        return sWord
    if '/' not in sAffCode:
        return sAffCode
    sPfxCode, sSfxCode = sAffCode.split('/')
    sWord = sPfxCode[1:] + sWord[(ord(sPfxCode[0])-48):]
    return sWord[:-(ord(sSfxCode[0])-48)] + sSfxCode[1:]  if sSfxCode[0] != '0'  else sWord + sSfxCode[1:]
