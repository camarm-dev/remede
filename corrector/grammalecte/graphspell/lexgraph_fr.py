"""
Lexicographer for the French language
"""

# Note:
# This mode must contains at least:
#     <dSugg> : a dictionary for default suggestions.
#     <bLexicographer> : a boolean False
#       if the boolean is True, 4 functions are required:
#           split(sWord) -> returns a list of string (that will be analyzed)
#           analyze(sWord) -> returns a string with the meaning of word
#           readableMorph(sMorph) -> returns a string with the meaning of tags
#           setLabelsOnToken(dToken) -> adds readable information on token
#           isValidSugg(sWord, oSpellChecker) -> returns a filtered list of suggestions


import re

#### Suggestions

dSugg = {
    "bcp": "beaucoup",
    "ca": "ça",
    "cad": "c’est-à-dire",
    "cb": "combien|CB",
    "cdlt": "cordialement",
    "construirent": "construire|construisirent|construisent|construiront",
    "càd": "c’est-à-dire",
    "chai": "j’sais|je sais",
    "chais": "j’sais|je sais",
    "chui": "j’suis|je suis",
    "chuis": "j’suis|je suis",
    "done": "donc|donne",
    "dc": "de|donc",
    "email": "courriel|e-mail|émail",
    "emails": "courriels|e-mails",
    "ete": "êtes|été",
    "Etes-vous": "Êtes-vous",
    "Etiez-vous": "Étiez-vous",
    "Etions-nous": "Étions-nous",
    "loins": "loin",
    "mn": "min",
    "mns": "min",
    "online": "en ligne",
    "parce-que": "parce que",
    "pcq": "parce que",
    "pd": "pendant",
    "pdq": "pendant que",
    "pdt": "pendant",
    "pdtq": "pendant que",
    "pécunier": "pécuniaire",
    "pécuniers": "pécuniaires",
    "pk": "pourquoi",
    "pkoi": "pourquoi",
    "pq": "pourquoi|PQ",
    "prq": "presque",
    "prsq": "presque",
    "qcq": "quiconque",
    "qd": "quand",
    "qq": "quelque",
    "qqch": "quelque chose",
    "qqn": "quelqu’un",
    "qqne": "quelqu’une",
    "qqs": "quelques",
    "qqunes": "quelques-unes",
    "qquns": "quelques-uns",
    "tdq": "tandis que",
    "tj": "toujours",
    "tjs": "toujours",
    "tq": "tant que|tandis que",
    "ts": "tous",
    "tt": "tant|tout",
    "tte": "toute",
    "ttes": "toutes",
    "y’a": "y a",

    "Iier": "Iᵉʳ",
    "Iière": "Iʳᵉ",
    "IIième": "IIᵉ",
    "IIIième": "IIIᵉ",
    "IVième": "IVᵉ",
    "Vième": "Vᵉ",
    "VIième": "VIᵉ",
    "VIIième": "VIIᵉ",
    "VIIIième": "VIIIᵉ",
    "IXième": "IXᵉ",
    "Xième": "Xᵉ",
    "XIième": "XIᵉ",
    "XIIième": "XIIᵉ",
    "XIIIième": "XIIIᵉ",
    "XIVième": "XIVᵉ",
    "XVième": "XVᵉ",
    "XVIième": "XVIᵉ",
    "XVIIième": "XVIIᵉ",
    "XVIIIième": "XVIIIᵉ",
    "XIXième": "XIXᵉ",
    "XXième": "XXᵉ",
    "XXIième": "XXIᵉ",
    "XXIIième": "XXIIᵉ",
    "XXIIIième": "XXIIIᵉ",
    "XXIVième": "XXIVᵉ",
    "XXVième": "XXVᵉ",
    "XXVIième": "XXVIᵉ",
    "XXVIIième": "XXVIIᵉ",
    "XXVIIIième": "XXVIIIᵉ",
    "XXIXième": "XXIXᵉ",
    "XXXième": "XXXᵉ",

    "Ier": "Iᵉʳ",
    "Ière": "Iʳᵉ",
    "IIème": "IIᵉ",
    "IIIème": "IIIᵉ",
    "IVème": "IVᵉ",
    "Vème": "Vᵉ",
    "VIème": "VIᵉ",
    "VIIème": "VIIᵉ",
    "VIIIème": "VIIIᵉ",
    "IXème": "IXᵉ",
    "Xème": "Xᵉ",
    "XIème": "XIᵉ",
    "XIIème": "XIIᵉ",
    "XIIIème": "XIIIᵉ",
    "XIVème": "XIVᵉ",
    "XVème": "XVᵉ",
    "XVIème": "XVIᵉ",
    "XVIIème": "XVIIᵉ",
    "XVIIIème": "XVIIIᵉ",
    "XIXème": "XIXᵉ",
    "XXème": "XXᵉ",
    "XXIème": "XXIᵉ",
    "XXIIème": "XXIIᵉ",
    "XXIIIème": "XXIIIᵉ",
    "XXIVème": "XXIVᵉ",
    "XXVème": "XXVᵉ",
    "XXVIème": "XXVIᵉ",
    "XXVIIème": "XXVIIᵉ",
    "XXVIIIème": "XXVIIIᵉ",
    "XXIXème": "XXIXᵉ",
    "XXXème": "XXXᵉ"
}


# Préfixes et suffixes

aPfx1 = frozenset([
    "anti", "archi", "contre", "hyper", "mé", "méta", "im", "in", "ir", "par", "proto",
    "pseudo", "pré", "re", "ré", "sans", "sous", "supra", "sur", "ultra"
])
aPfx2 = frozenset([
    "belgo", "franco", "génito", "gynéco", "médico", "russo"
])


#### Lexicographer

bLexicographer = True

_dTAGS = {
    ':N': (" nom,", "Nom"),
    ':A': (" adjectif,", "Adjectif"),
    ':M1': (" prénom,", "Prénom"),
    ':M2': (" patronyme,", "Patronyme, matronyme, nom de famille…"),
    ':MP': (" nom propre,", "Nom propre"),
    ':W': (" adverbe,", "Adverbe"),
    ':J': (" interjection,", "Interjection"),
    ':B': (" nombre,", "Nombre"),
    ':Br': (" nombre romain,", "Nombre romain"),
    ':T': (" titre,", "Titre de civilité"),

    ':e': (" épicène", "épicène"),
    ':m': (" masculin", "masculin"),
    ':f': (" féminin", "féminin"),
    ':s': (" singulier", "singulier"),
    ':p': (" pluriel", "pluriel"),
    ':i': (" invariable", "invariable"),

    ':V1_': (" verbe (1ᵉʳ gr.),", "Verbe du 1ᵉʳ groupe"),
    ':V2_': (" verbe (2ᵉ gr.),", "Verbe du 2ᵉ groupe"),
    ':V3_': (" verbe (3ᵉ gr.),", "Verbe du 3ᵉ groupe"),
    ':V1e': (" verbe (1ᵉʳ gr.),", "Verbe du 1ᵉʳ groupe"),
    ':V2e': (" verbe (2ᵉ gr.),", "Verbe du 2ᵉ groupe"),
    ':V3e': (" verbe (3ᵉ gr.),", "Verbe du 3ᵉ groupe"),
    ':V0e': (" verbe,", "Verbe auxiliaire être"),
    ':V0a': (" verbe,", "Verbe auxiliaire avoir"),

    ':Y': (" infinitif,", "infinitif"),
    ':P': (" participe présent,", "participe présent"),
    ':Q': (" participe passé,", "participe passé"),
    ':Ip': (" présent,", "indicatif présent"),
    ':Iq': (" imparfait,", "indicatif imparfait"),
    ':Is': (" passé simple,", "indicatif passé simple"),
    ':If': (" futur,", "indicatif futur"),
    ':K': (" conditionnel présent,", "conditionnel présent"),
    ':Sp': (" subjonctif présent,", "subjonctif présent"),
    ':Sq': (" subjonctif imparfait,", "subjonctif imparfait"),
    ':E': (" impératif,", "impératif"),

    ':1s': (" 1ʳᵉ p. sg.,", "verbe : 1ʳᵉ personne du singulier"),
    ':1ŝ': (" présent interr. 1ʳᵉ p. sg.,", "verbe : 1ʳᵉ personne du singulier (présent interrogatif)"),
    ':1ś': (" présent interr. 1ʳᵉ p. sg.,", "verbe : 1ʳᵉ personne du singulier (présent interrogatif)"),
    ':2s': (" 2ᵉ p. sg.,", "verbe : 2ᵉ personne du singulier"),
    ':3s': (" 3ᵉ p. sg.,", "verbe : 3ᵉ personne du singulier"),
    ':1p': (" 1ʳᵉ p. pl.,", "verbe : 1ʳᵉ personne du pluriel"),
    ':2p': (" 2ᵉ p. pl.,", "verbe : 2ᵉ personne du pluriel"),
    ':3p': (" 3ᵉ p. pl.,", "verbe : 3ᵉ personne du pluriel"),
    ':3p!': (" 3ᵉ p. pl.,", "verbe : 3ᵉ personne du pluriel"),

    ':G': ("[mot grammatical]", "Mot grammatical"),
    ':X': (" adverbe de négation,", "Adverbe de négation"),
    ':U': (" adverbe interrogatif,", "Adverbe interrogatif"),
    ':R': (" préposition,", "Préposition"),
    ':Rv': (" préposition verbale,", "Préposition verbale"),
    ':D': (" déterminant,", "Déterminant"),
    ':Dd': (" déterminant démonstratif,", "Déterminant démonstratif"),
    ':De': (" déterminant exclamatif,", "Déterminant exclamatif"),
    ':Dp': (" déterminant possessif,", "Déterminant possessif"),
    ':Di': (" déterminant indéfini,", "Déterminant indéfini"),
    ':Dn': (" déterminant négatif,", "Déterminant négatif"),
    ':Od': (" pronom démonstratif,", "Pronom démonstratif"),
    ':Oi': (" pronom indéfini,", "Pronom indéfini"),
    ':On': (" pronom indéfini négatif,", "Pronom indéfini négatif"),
    ':Ot': (" pronom interrogatif,", "Pronom interrogatif"),
    ':Or': (" pronom relatif,", "Pronom relatif"),
    ':Ow': (" pronom adverbial,", "Pronom adverbial"),
    ':Os': (" pronom personnel sujet,", "Pronom personnel sujet"),
    ':Oo': (" pronom personnel objet,", "Pronom personnel objet"),
    ':Ov': (" préverbe,", "Préverbe"),
    ':O1': (" 1ʳᵉ pers.,", "Pronom : 1ʳᵉ personne"),
    ':O2': (" 2ᵉ pers.,", "Pronom : 2ᵉ personne"),
    ':O3': (" 3ᵉ pers.,", "Pronom : 3ᵉ personne"),
    ':C': (" conjonction,", "Conjonction"),
    ':Cc': (" conjonction de coordination,", "Conjonction de coordination"),
    ':Cs': (" conjonction de subordination,", "Conjonction de subordination"),

    ':ÉC': (" élément de conjonction,", "Élément de conjonction"),
    ':ÉCs': (" élément de conjonction de subordination,", "Élément de conjonction de subordination"),
    ':ÉN': (" élément de locution nominale,", "Élément de locution nominale"),
    ':ÉA': (" élément de locution adjectivale,", "Élément de locution adjectivale"),
    ':ÉV': (" élément de locution verbale,", "Élément de locution verbale"),
    ':ÉW': (" élément de locution adverbiale,", "Élément de locution adverbiale"),
    ':ÉR': (" élément de locution prépositive,", "Élément de locution prépositive"),
    ':ÉJ': (" élément de locution interjective,", "Élément de locution interjective"),

    ':L': (" locution", "Locution"),
    ':LN': (" locution nominale", "Locution nominale"),
    ':LA': (" locution adjectivale", "Locution adjectivale"),
    ':LV': (" locution verbale", "Locution verbale"),
    ':LW': (" locution adverbiale", "Locution adverbiale"),
    ':LR': (" locution prépositive", "Locution prépositive"),
    ':LRv': (" locution prépositive verbale", "Locution prépositive verbale"),
    ':LO': (" locution pronominale", "Locution pronominale"),
    ':LC': (" locution conjonctive", "Locution conjonctive"),
    ':LJ': (" locution interjective", "Locution interjective"),

    ':Zp': (" préfixe,", "Préfixe"),
    ':Zs': (" suffixe,", "Suffixe"),

    ':H': ("", "<Hors-norme, inclassable>"),
    ':HEL': (" lettre ‹l› euphonique", "Lettre ‹l› euphonique"),

    ':@': ("", "<Caractère non alpha-numérique>"),
    ':@p': (" signe de ponctuation", "Signe de ponctuation"),
    ':@s': (" signe", "Signe divers"),

    ';S': (" : symbole (unité de mesure)", "Symbole (unité de mesure)"),
    ';C': (" : couleur", "Couleur"),
    ';É': ("", "Élision requise"),
    ';é': ("", "Pas d’élision"),

    '#G': (" : gentilé", "Gentilé"),
    '#L': ("", "Langue"),
    '#C': (" : cité", "Cité"),
    '#P': (" : pays", "Pays"),

    '/*': ("", "Sous-dictionnaire <Commun>"),
    '/C': (" <classique>", "Sous-dictionnaire <Classique>"),
    '/M': ("", "Sous-dictionnaire <Moderne>"),
    '/R': (" <réforme>", "Sous-dictionnaire <Réforme 1990>"),
    '/A': ("", "Sous-dictionnaire <Annexe>"),
    '/X': ("", "Sous-dictionnaire <Contributeurs>")
}

_dValues = {
    '-je': " pronom personnel sujet, 1ʳᵉ pers. sing.",
    '-tu': " pronom personnel sujet, 2ᵉ pers. sing.",
    '-il': " pronom personnel sujet, 3ᵉ pers. masc. sing.",
    '-iel': " pronom personnel sujet, 3ᵉ pers. sing.",
    '-on': " pronom personnel sujet, 3ᵉ pers. sing. ou plur.",
    '-ce': " pronom personnel sujet, 3ᵉ pers. sing. ou plur.",
    '-elle': " pronom personnel sujet, 3ᵉ pers. fém. sing.",
    '-t-il': " “t” euphonique + pronom personnel sujet, 3ᵉ pers. masc. sing.",
    '-t-on': " “t” euphonique + pronom personnel sujet, 3ᵉ pers. sing. ou plur.",
    '-t-elle': " “t” euphonique + pronom personnel sujet, 3ᵉ pers. fém. sing.",
    '-t-iel': " “t” euphonique + pronom personnel sujet, 3ᵉ pers. sing.",
    '-nous': " pronom personnel sujet/objet, 1ʳᵉ pers. plur.  ou  COI (à nous), plur.",
    '-vous': " pronom personnel sujet/objet, 2ᵉ pers. plur.  ou  COI (à vous), plur.",
    '-ils': " pronom personnel sujet, 3ᵉ pers. masc. plur.",
    '-elles': " pronom personnel sujet, 3ᵉ pers. masc. plur.",
    '-iels': " pronom personnel sujet, 3ᵉ pers. plur.",

    "-là": " particule démonstrative (là)",
    "-ci": " particule démonstrative (ci)",

    '-le': " COD, masc. sing.",
    '-la': " COD, fém. sing.",
    '-les': " COD, plur.",

    '-moi': " COI (à moi), sing.",
    '-toi': " COI (à toi), sing.",
    '-lui': " COI (à lui ou à elle), sing.",
    '-leur': " COI (à eux ou à elles), plur.",

    '-le-moi': " COD, masc. sing. + COI (à moi), sing.",
    '-le-toi': " COD, masc. sing. + COI (à toi), sing.",
    '-le-lui': " COD, masc. sing. + COI (à lui ou à elle), sing.",
    '-le-nous': " COD, masc. sing. + COI (à nous), plur.",
    '-le-vous': " COD, masc. sing. + COI (à vous), plur.",
    '-le-leur': " COD, masc. sing. + COI (à eux ou à elles), plur.",

    '-la-moi': " COD, fém. sing. + COI (à moi), sing.",
    '-la-toi': " COD, fém. sing. + COI (à toi), sing.",
    '-la-lui': " COD, fém. sing. + COI (à lui ou à elle), sing.",
    '-la-nous': " COD, fém. sing. + COI (à nous), plur.",
    '-la-vous': " COD, fém. sing. + COI (à vous), plur.",
    '-la-leur': " COD, fém. sing. + COI (à eux ou à elles), plur.",

    '-les-moi': " COD, plur. + COI (à moi), sing.",
    '-les-toi': " COD, plur. + COI (à toi), sing.",
    '-les-lui': " COD, plur. + COI (à lui ou à elle), sing.",
    '-les-nous': " COD, plur. + COI (à nous), plur.",
    '-les-vous': " COD, plur. + COI (à vous), plur.",
    '-les-leur': " COD, plur. + COI (à eux ou à elles), plur.",

    '-y': " pronom adverbial",
    "-m’y": " (me) pronom personnel objet + (y) pronom adverbial",
    "-t’y": " (te) pronom personnel objet + (y) pronom adverbial",
    "-s’y": " (se) pronom personnel objet + (y) pronom adverbial",

    '-en': " pronom adverbial",
    "-m’en": " (me) pronom personnel objet + (en) pronom adverbial",
    "-t’en": " (te) pronom personnel objet + (en) pronom adverbial",
    "-s’en": " (se) pronom personnel objet + (en) pronom adverbial",

    '.': "point",
    '·': "point médian",
    '…': "points de suspension",
    ':': "deux-points",
    ';': "point-virgule",
    ',': "virgule",
    '?': "point d’interrogation",
    '!': "point d’exclamation",
    '(': "parenthèse ouvrante",
    ')': "parenthèse fermante",
    '[': "crochet ouvrant",
    ']': "crochet fermant",
    '{': "accolade ouvrante",
    '}': "accolade fermante",
    '-': "tiret",
    '—': "tiret cadratin",
    '–': "tiret demi-cadratin",
    '«': "guillemet ouvrant (chevrons)",
    '»': "guillemet fermant (chevrons)",
    '“': "guillemet ouvrant double",
    '”': "guillemet fermant double",
    '‘': "guillemet ouvrant",
    '’': "guillemet fermant",
    '"': "guillemets droits (déconseillé en typographie)",
    '/': "signe de la division",
    '+': "signe de l’addition",
    '*': "signe de la multiplication",
    '=': "signe de l’égalité",
    '<': "inférieur à",
    '>': "supérieur à",
    '⩽': "inférieur ou égal à",
    '⩾': "supérieur ou égal à",
    '%': "signe de pourcentage",
    '‰': "signe pour mille"
}


_zElidedPrefix = re.compile("(?i)^([ldmtsnjcç]|lorsqu|presqu|jusqu|puisqu|quoiqu|quelqu|qu)[’'‘`ʼ]([\\w-]+)")
_zCompoundWord = re.compile("(?i)(\\w+)(-(?:(?:les?|la)-(?:moi|toi|lui|[nv]ous|leur)|t-(?:il|elle|on)|y|en|[mts]’(?:y|en)|les?|l[aà]|[mt]oi|leur|lui|je|tu|ils?|elles?|on|[nv]ous|ce))$")
_zTag = re.compile("[:;/#][\\w@*!][^:;/#]*")

def split (sWord):
    "split word in 3 parts: prefix, root, suffix"
    sPrefix = ""
    sSuffix = ""
    # préfixe élidé
    m = _zElidedPrefix.match(sWord)
    if m:
        sPrefix = m.group(1) + "’"
        sWord = m.group(2)
    # mots composés
    m = _zCompoundWord.match(sWord)
    if m:
        sWord = m.group(1)
        sSuffix = m.group(2)
    return sPrefix, sWord, sSuffix


def analyze (sWord):
    "return meaning of <sWord> if found else an empty string"
    sWord = sWord.lower()
    if sWord in _dValues:
        return _dValues[sWord]
    return ""


def readableMorph (sMorph):
    "returns string: readable tags"
    if not sMorph:
        return "mot inconnu"
    sRes = ""
    sVType = ""
    if ":V" in sMorph:
        sMorph = re.sub("(?<=V[0123][ea_])[itpqnmr_eaxz]+", "", sMorph)
    if ":Q" in sMorph:
        nVerbTag = sMorph.find(":V")
        sVType = sMorph[nVerbTag:nVerbTag+4]
        sMorph = sMorph[4:].replace(":1ŝ", "").replace(":1ś", "")
    for m in _zTag.finditer(sMorph):
        sRes += _readableTag(m.group(0))
    if sRes.startswith((" verbe", " participe")) and not sRes.endswith("infinitif"):
        if sVType:
            sRes += " [" + sMorph[1:sMorph.find("/")] + " : " + _readableTag(sVType).rstrip(",") + "]"
        else:
            sRes += " [" + sMorph[1:sMorph.find("/")] + "]"
    if not sRes:
        return " [" + sMorph + "]: étiquettes inconnues"
    return sRes.rstrip(",")

def _readableTag (sTag):
    "returns string: readable tag"
    if sTag in _dTAGS:
        return _dTAGS[sTag][0]
    return " [" + sTag + "]?"


_zPartDemForm = re.compile("([\\w]+)-(là|ci)$")
_zInterroVerb = re.compile("([\\w]+)(-(?:t-(?:ie?l|elle|on)|je|tu|ie?ls?|elles?|on|[nv]ous))$")
_zImperatifVerb = re.compile("([\\w]+)(-(?:l(?:es?|a)-(?:moi|toi|lui|[nv]ous|leur)|y|en|[mts]['’ʼ‘‛´`′‵՚ꞌꞋ](?:y|en)|les?|la|[mt]oi|leur|lui))$")

def setLabelsOnToken (dToken):
    "create an attribute “alabels” on <dToken> as a list of readable meanings"
    # Token: .sType, .sValue, .nStart, .nEnd, .lMorph
    try:
        if dToken["sType"] == "PUNC" or dToken["sType"] == "SIGN":
            dToken["aLabels"] = [ _dValues.get(dToken["sValue"], "signe de ponctuation divers") ]
        elif dToken["sType"] == 'SYMBOL':
            dToken["aLabels"] = ["symbole"]
        elif dToken["sType"] == 'EMOJI':
            dToken["aLabels"] = ["émoji"]
        elif dToken["sType"] == 'NUM':
            dToken["aLabels"] = ["nombre"]
        elif dToken["sType"] == 'LINK':
            dToken["aLabels"] = ["hyperlien"]
        elif dToken["sType"] == 'TAG':
            dToken["aLabels"] = ["étiquette (hashtag)"]
        elif dToken["sType"] == 'HTML':
            dToken["aLabels"] = ["balise HTML"]
        elif dToken["sType"] == 'PSEUDOHTML':
            dToken["aLabels"] = ["balise pseudo-HTML"]
        elif dToken["sType"] == 'HTMLENTITY':
            dToken["aLabels"] = ["entité caractère XML/HTML"]
        elif dToken["sType"] == 'HOUR':
            dToken["aLabels"] = ["heure"]
        elif dToken["sType"] == 'WORDORD':
            dToken["aLabels"] = ["nombre ordinal"]
        elif dToken["sType"] == 'FOLDERUNIX':
            dToken["aLabels"] = ["dossier UNIX (et dérivés)"]
        elif dToken["sType"] == 'FOLDERWIN':
            dToken["aLabels"] = ["dossier Windows"]
        elif dToken["sType"] == 'WORD_ACRONYM':
            dToken["aLabels"] = ["sigle ou acronyme"]
        elif dToken["sType"] == 'WORD' or dToken["sType"] == 'WORDELD':
            if "lMorph" in dToken and dToken["lMorph"]:
                # with morphology
                dToken["aLabels"] = []
                for sMorph in dToken["lMorph"]:
                    dToken["aLabels"].append(readableMorph(sMorph))
            else:
                # no morphology, guessing
                if dToken["sValue"].count("-") > 4:
                    dToken["aLabels"] = ["élément complexe indéterminé"]
                elif _zPartDemForm.search(dToken["sValue"]):
                    # mots avec particules démonstratives
                    dToken["aLabels"] = ["mot avec particule démonstrative"]
                elif _zImperatifVerb.search(dToken["sValue"]):
                    # formes interrogatives
                    dToken["aLabels"] = ["forme verbale impérative"]
                elif _zInterroVerb.search(dToken["sValue"]):
                    # formes interrogatives
                    dToken["aLabels"] = ["forme verbale interrogative"]
                else:
                    dToken["aLabels"] = ["mot inconnu du dictionnaire"]
            if "lSubTokens" in dToken:
                for dSubToken in dToken["lSubTokens"]:
                    if dSubToken["sValue"]:
                        if dSubToken["sValue"] in _dValues:
                            dSubToken["lMorph"] = [ "" ]
                            dSubToken["aLabels"] = [ _dValues[dSubToken["sValue"]] ]
                        else:
                            dSubToken["aLabels"] = [ readableMorph(sMorph)  for sMorph in dSubToken["lMorph"] ]
        else:
            dToken["aLabels"] = ["token de nature inconnue"]
    except:
        return


# Other functions

def isValidSugg (sSugg, oSpellChecker):
    "return True if <sSugg> is valid"
    if sSugg.endswith(("è", "È")):
        return False
    if "’" in sSugg:
        if sSugg.startswith(("d’", "D’")) and not oSpellChecker.morph(sSugg[2:], ":[YNAW]"):
            return False
        if sSugg.startswith(("n’", "m’", "t’", "s’", "N’", "M’", "T’", "S’")) and not oSpellChecker.morph(sSugg[2:], ":V"):
            return False
        if sSugg.startswith(("j’", "J’")) and not oSpellChecker.morph(sSugg[2:], ":(?:Y|[123][sp])"):
            return False
        if sSugg.startswith(("c’", "C’")) and not oSpellChecker.morph(sSugg[2:], ":3[sp]"):
            return False
    return True
