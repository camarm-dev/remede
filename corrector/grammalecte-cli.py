#!/usr/bin/env python3

"""
Grammalecte CLI (command line interface)
"""

import sys
import os.path
import argparse
import json
import itertools
import re
import traceback

import grammalecte
import grammalecte.text as txt
import grammalecte.graphspell.str_transform as strt
from grammalecte.graphspell.echo import echo


_EXAMPLE = "Quoi ? Racontes ! Racontes-moi ! Bon sangg, parles ! Oui. Il y a des menteur partout. " \
           "Je suit sidéré par la brutales arrogance de cette homme-là. Quelle salopard ! Un escrocs de la pire espece. " \
           "Quant sera t’il châtiés pour ses mensonge ?             Merde ! J’en aie marre."

_HELP = """
Analysis commands:
    any_text                            grammar checking
    ?word1 [word2] ...                  words analysis
    !word                               spelling suggestion
    >word                               draw path of word in the word graph
    =[filter1][=[filter2]]              show entries which fit to filters (filter1 for word, filter2 for morphology)
    ≠word|word|…                        show distance between words
    $some_text                          show sentences and tokens of text

Other commands:
    /help                       /h      show this text
    /lopt                       /lo     list options
    /lrules [pattern]           /lr     list rules
    /o+ option1 [option2] ...           activate grammar checking options
    /o- option1 [option2] ...           deactivate grammar checking options
    /r+ rule1 [rule2] ...               reactivate grammar checking rule
    /r- rule1 [rule2] ...               deactivate grammar checking rule
    /textformatter              /tf     switch on/off the text formatter
    /debug                      /d      switch on/off the debug mode
    /quit                       /q      exit
"""


def _getText (sInputText):
    sText = input(sInputText)
    if sText == "*":
        return _EXAMPLE
    if sys.platform == "win32":
        # Apparently, the console transforms «’» in «'».
        # So we reverse it to avoid many useless warnings.
        sText = sText.replace("'", "’")
    return sText


def readFile (spf):
    "generator: returns file line by line"
    if os.path.isfile(spf):
        with open(spf, "r", encoding="utf-8") as hSrc:
            for sLine in hSrc:
                yield sLine
    else:
        print("# Error: file <" + spf + "> not found.")


def generateParagraphFromFile (spf, bConcatLines=False):
    "generator: returns text by tuple of (iParagraph, sParagraph, lLineSet)"
    if not bConcatLines:
        for iParagraph, sLine in enumerate(readFile(spf), 1):
            yield iParagraph, sLine, None
    else:
        lLine = []
        iParagraph = 1
        for iLine, sLine in enumerate(readFile(spf), 1):
            if sLine.strip():
                lLine.append((iLine, sLine))
            elif lLine:
                sText, lLineSet = txt.createParagraphWithLines(lLine)
                yield iParagraph, sText, lLineSet
                lLine = []
            iParagraph += 1
        if lLine:
            sText, lLineSet = txt.createParagraphWithLines(lLine)
            yield iParagraph, sText, lLineSet


def output (sText, hDst=None):
    "write in the console or in a file if <hDst> not null"
    if not hDst:
        echo(sText, end="")
    else:
        hDst.write(sText)


def loadDictionary (spf):
    "returns the dictionary as a dictionary object"
    if os.path.isfile(spf):
        sJSON = open(spf, "r", encoding="utf-8").read()
        try:
            oJSON = json.loads(sJSON)
        except json.JSONDecodeError:
            print("# Error. File <" + spf + " is not a valid JSON file.")
            return None
        return oJSON
    print("# Error: file <" + spf + "> not found.")
    return None


def getCommand ():
    while True:
        print("COMMANDS: [N]ext paragraph  [Q]uit.")
        print("          [Error number]>[suggestion number]")
        print("          [Error number] (apply first suggestion)")
        print("          [Error number]=[replacement]")
        sCommand = input("        ? ")
        if sCommand == "q" or sCommand == "Q" or sCommand == "n" or sCommand == "N":
            return sCommand
        elif re.match("^([0-9]+)(>[0-9]*|=.*|)$", sCommand):
            m = re.match("^([0-9]+)(>[0-9]*|=.*|)$", sCommand)
            nError = int(m.group(1)) - 1
            cAction = m.group(2)[0:1] or ">"
            if cAction == ">":
                vSugg = int(m.group(2)[1:]) - 1  if m.group(2)  else 0
            else:
                vSugg = m.group(2)[1:]
            return (nError, cAction, vSugg)


def main ():
    "launch the CLI (command line interface)"
    if sys.version_info < (3, 5):
        print("Python 3.5+ required")
        return

    xParser = argparse.ArgumentParser()
    xParser.add_argument("-f", "--file", help="parse file (UTF-8 required!) [on Windows, -f is similar to -ff]", type=str)
    xParser.add_argument("-ff", "--file_to_file", help="parse file (UTF-8 required!) and create a result file (*.res.txt)", type=str)
    xParser.add_argument("-iff", "--interactive_file_to_file", help="parse file (UTF-8 required!) and create a result file (*.res.txt)", type=str)
    xParser.add_argument("-owe", "--only_when_errors", help="display results only when there are errors", action="store_true")
    xParser.add_argument("-j", "--json", help="generate list of errors in JSON (only with option --file or --file_to_file)", action="store_true")
    xParser.add_argument("-cl", "--concat_lines", help="concatenate lines not separated by an empty paragraph (only with option --file or --file_to_file)", action="store_true")
    xParser.add_argument("-tf", "--textformatter", help="auto-format text according to typographical rules (not with option --concat_lines)", action="store_true")
    xParser.add_argument("-tfo", "--textformatteronly", help="auto-format text and disable grammar checking (only with option --file or --file_to_file)", action="store_true")
    xParser.add_argument("-ctx", "--context", help="return errors with context (only with option --json)", action="store_true")
    xParser.add_argument("-wss", "--with_spell_sugg", help="add suggestions for spelling errors (only with option --file or --file_to_file)", action="store_true")
    xParser.add_argument("-pdi", "--personal_dict", help="load personnal dictionary (JSON file)", type=str)
    xParser.add_argument("-w", "--width", help="width in characters (40 < width < 200; default: 100)", type=int, choices=range(40,201,10), default=100)
    xParser.add_argument("-lo", "--list_options", help="list options", action="store_true")
    xParser.add_argument("-lr", "--list_rules", nargs="?", help="list rules [regex pattern as filter]", const="*")
    xParser.add_argument("-sug", "--suggest", help="get suggestions list for given word", type=str)
    xParser.add_argument("-on", "--opt_on", nargs="+", help="activate options")
    xParser.add_argument("-off", "--opt_off", nargs="+", help="deactivate options")
    xParser.add_argument("-roff", "--rule_off", nargs="+", help="deactivate rules")
    xParser.add_argument("-d", "--debug", help="debugging mode (only in interactive mode)", action="store_true")
    xArgs = xParser.parse_args()

    oGrammarChecker = grammalecte.GrammarChecker("fr")
    oSpellChecker = oGrammarChecker.getSpellChecker()
    oTextFormatter = oGrammarChecker.getTextFormatter()
    if xArgs.personal_dict:
        oJSON = loadDictionary(xArgs.personal_dict)
        if oJSON:
            oSpellChecker.setPersonalDictionary(oJSON)

    if not xArgs.json:
        echo("Python v" + sys.version)
        echo("Grammalecte v{}".format(oGrammarChecker.gce.version))

    # list options or rules
    if xArgs.list_options or xArgs.list_rules:
        if xArgs.list_options:
            oGrammarChecker.gce.displayOptions("fr")
        if xArgs.list_rules:
            oGrammarChecker.gce.displayRules(None  if xArgs.list_rules == "*"  else xArgs.list_rules)
        exit()

    # spell suggestions
    if xArgs.suggest:
        for lSugg in oSpellChecker.suggest(xArgs.suggest):
            if xArgs.json:
                sText = json.dumps({ "aSuggestions": lSugg }, ensure_ascii=False)
            else:
                sText = "Suggestions : " + " | ".join(lSugg)
            echo(sText)
        exit()

    # disable options
    if not xArgs.json:
        xArgs.context = False
    if xArgs.concat_lines:
        xArgs.textformatter = False

    # grammar options
    oGrammarChecker.gce.setOptions({"html": True, "latex": True})
    if xArgs.opt_on:
        oGrammarChecker.gce.setOptions({ opt:True  for opt in xArgs.opt_on })
    if xArgs.opt_off:
        oGrammarChecker.gce.setOptions({ opt:False  for opt in xArgs.opt_off })

    # disable grammar rules
    if xArgs.rule_off:
        for sRule in xArgs.rule_off:
            oGrammarChecker.gce.ignoreRule(sRule)


    if xArgs.file or xArgs.file_to_file:
        # file processing
        sFile = xArgs.file or xArgs.file_to_file
        hDst = open(sFile[:sFile.rfind(".")]+".res.txt", "w", encoding="utf-8", newline="\n")  if xArgs.file_to_file or sys.platform == "win32"  else None
        bComma = False
        if xArgs.json:
            output('{ "grammalecte": "'+oGrammarChecker.gce.version+'", "lang": "'+oGrammarChecker.gce.lang+'", "data" : [\n', hDst)
        for i, sText, lLineSet in generateParagraphFromFile(sFile, xArgs.concat_lines):
            if xArgs.textformatter or xArgs.textformatteronly:
                sText = oTextFormatter.formatText(sText)
            if xArgs.textformatteronly:
                output(sText, hDst)
                continue
            if xArgs.json:
                sText = oGrammarChecker.getParagraphErrorsAsJSON(i, sText, bContext=xArgs.context, bEmptyIfNoErrors=xArgs.only_when_errors, \
                                                                bSpellSugg=xArgs.with_spell_sugg, bReturnText=xArgs.textformatter, lLineSet=lLineSet)
            else:
                sText, _ = oGrammarChecker.getParagraphWithErrors(sText, bEmptyIfNoErrors=xArgs.only_when_errors, bSpellSugg=xArgs.with_spell_sugg, nWidth=xArgs.width)
            if sText:
                if xArgs.json and bComma:
                    output(",\n", hDst)
                output(sText, hDst)
                bComma = True
            if hDst:
                echo("§ %d\r" % i, end="", flush=True)
        if xArgs.json:
            output("\n]}\n", hDst)
    elif xArgs.interactive_file_to_file:
        # file processing: interactive mode
        sFile = xArgs.interactive_file_to_file
        hDst = open(sFile[:sFile.rfind(".")]+".res.txt", "w", encoding="utf-8", newline="\n")
        for i, sText, lLineSet in generateParagraphFromFile(sFile, xArgs.concat_lines):
            if xArgs.textformatter:
                sText = oTextFormatter.formatText(sText)
            while True:
                sResult, lErrors = oGrammarChecker.getParagraphWithErrors(sText, bEmptyIfNoErrors=False, bSpellSugg=True, nWidth=xArgs.width)
                print("\n\n============================== Paragraph " + str(i) + " ==============================\n")
                echo(sResult)
                print("\n")
                vCommand = getCommand()
                if vCommand == "q":
                    # quit
                    hDst.close()
                    exit()
                elif vCommand == "n":
                    # next paragraph
                    hDst.write(sText)
                    break
                else:
                    nError, cAction, vSugg = vCommand
                    if 0 <= nError <= len(lErrors) - 1:
                        dErr = lErrors[nError]
                        if cAction == ">"  and  0 <= vSugg <= len(dErr["aSuggestions"]) - 1:
                            sSugg = dErr["aSuggestions"][vSugg]
                            sText = sText[0:dErr["nStart"]] + sSugg + sText[dErr["nEnd"]:]
                        elif cAction == "=":
                            sText = sText[0:dErr["nStart"]] + vSugg + sText[dErr["nEnd"]:]
                        else:
                            print("Error. Action not possible.")
                    else:
                        print("Error. This error doesn’t exist.")
    else:
        # pseudo-console
        sInputText = "\n~==========~ Enter your text [/h /q] ~==========~\n"
        sText = _getText(sInputText)
        while True:
            if sText.startswith("?"):
                for sWord in sText[1:].strip().split():
                    if sWord:
                        echo("* " + sWord)
                        for sElem, aRes in oSpellChecker.analyze(sWord):
                            echo("  - " + sElem)
                            for sMorph, sMeaning in aRes:
                                echo("      {:<40}  {}".format(sMorph, sMeaning))
            elif sText.startswith("!"):
                for sWord in sText[1:].strip().split():
                    if sWord:
                        for lSugg in oSpellChecker.suggest(sWord):
                            echo(" | ".join(lSugg))
            elif sText.startswith(">"):
                oSpellChecker.drawPath(sText[1:].strip())
            elif sText.startswith("="):
                sSearch = sText[1:].strip()
                if "=" in sSearch:
                    nCut = sSearch.find("=")
                    sFlexPattern = sSearch[0:nCut]
                    sTagsPattern = sSearch[nCut+1:]
                else:
                    sFlexPattern = sSearch
                    sTagsPattern = ""
                for aRes in oSpellChecker.select(sFlexPattern, sTagsPattern):
                    echo("{:<30} {:<30} {}".format(*aRes))
            elif sText.startswith("≠"):
                lWords = sText[1:].split("|")
                for s1, s2 in itertools.combinations(lWords, 2):
                    nDist = strt.distanceDamerauLevenshtein(s1, s2)
                    print(f"{s1} ≠ {s2}: {nDist}")
            elif sText.startswith("/o+ "):
                oGrammarChecker.gce.setOptions({ opt:True  for opt in sText[3:].strip().split()  if opt in oGrammarChecker.gce.getOptions() })
                echo("done")
            elif sText.startswith("/o- "):
                oGrammarChecker.gce.setOptions({ opt:False  for opt in sText[3:].strip().split()  if opt in oGrammarChecker.gce.getOptions() })
                echo("done")
            elif sText.startswith("/r- "):
                for sRule in sText[3:].strip().split():
                    oGrammarChecker.gce.ignoreRule(sRule)
                echo("done")
            elif sText.startswith("/r+ "):
                for sRule in sText[3:].strip().split():
                    oGrammarChecker.gce.reactivateRule(sRule)
                echo("done")
            elif sText in ("/debug", "/d"):
                xArgs.debug = not xArgs.debug
                echo("debug mode on"  if xArgs.debug  else "debug mode off")
            elif sText in ("/textformatter", "/tf"):
                xArgs.textformatter = not xArgs.textformatter
                echo("textformatter on"  if xArgs.debug  else "textformatter off")
            elif sText in ("/help", "/h"):
                echo(_HELP)
            elif sText in ("/lopt", "/lo"):
                oGrammarChecker.gce.displayOptions("fr")
            elif sText.startswith("/lr"):
                sText = sText.strip()
                sFilter = sText[sText.find(" "):].strip()  if " " in sText  else None
                oGrammarChecker.gce.displayRules(sFilter)
            elif sText in ("/quit", "/q"):
                break
            elif sText.startswith("/rl"):
                # reload (todo)
                pass
            elif sText.startswith("$"):
                for sParagraph in txt.getParagraph(sText[1:]):
                    if xArgs.textformatter:
                        sParagraph = oTextFormatter.formatText(sParagraph)
                    lParagraphErrors, lSentences = oGrammarChecker.gce.parse(sParagraph, bDebug=xArgs.debug, bFullInfo=True)
                    #echo(txt.getReadableErrors(lParagraphErrors, xArgs.width))
                    for dSentence in lSentences:
                        echo("{nStart}:{nEnd}  <{sSentence}>".format(**dSentence))
                        for dToken in dSentence["lTokens"]:
                            if dToken["sType"] == "INFO" or "bMerged" in dToken:
                                continue
                            echo("  {0[nStart]:>3}:{0[nEnd]:<3} {1} {0[sType]:<14} {2} {0[sValue]:<16} {3}".format(dToken, \
                                                                                                        "×" if dToken.get("bToRemove", False) else " ",
                                                                                                        "!" if dToken["sType"] == "WORD" and not dToken.get("bValidToken", False) else " ",
                                                                                                        " ".join(dToken.get("aTags", "")) ) )
                            if "lMorph" in dToken:
                                for sMorph, sLabel in zip(dToken["lMorph"], dToken["aLabels"]):
                                    echo("            {0:40}  {1}".format(sMorph, sLabel))
                            if "lSubTokens" in dToken:
                                for dSubToken in dToken["lSubTokens"]:
                                    if dSubToken["sValue"]:
                                        echo("              · {0:20}".format(dSubToken["sValue"]))
                                        for sMorph, sLabel in zip(dSubToken["lMorph"], dSubToken["aLabels"]):
                                            echo("                {0:40}  {1}".format(sMorph, sLabel))
                        #echo(txt.getReadableErrors(dSentence["lGrammarErrors"], xArgs.width))
            else:
                if sText.startswith("TEST: "):
                    sText = sText[6:]
                    sText = sText.replace("{{", "").replace("}}", "")
                    sText = re.sub(" ->> .*$", "", sText).rstrip()
                for sParagraph in txt.getParagraph(sText):
                    if xArgs.textformatter:
                        sParagraph = oTextFormatter.formatText(sParagraph)
                    sRes, _ = oGrammarChecker.getParagraphWithErrors(sParagraph, bEmptyIfNoErrors=xArgs.only_when_errors, nWidth=xArgs.width, bDebug=xArgs.debug)
                    if sRes:
                        echo("\n" + sRes)
                    else:
                        echo("\nNo error found.")
            sText = _getText(sInputText)


if __name__ == '__main__':
    main()
