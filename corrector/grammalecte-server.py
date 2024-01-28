#!/usr/bin/env python3

"""
Grammalecte server: grammar checker
"""

import sys
import argparse
import json
import traceback
import time
import os
import concurrent.futures

from grammalecte.bottle import Bottle, run, request, response #, template, static_file

import grammalecte
import grammalecte.text as txt
from grammalecte.graphspell.echo import echo


#### GRAMMAR CHECKER ####

oGrammarChecker = grammalecte.GrammarChecker("fr", "Server")
oSpellChecker = oGrammarChecker.getSpellChecker()
oTextFormatter = oGrammarChecker.getTextFormatter()
oGCE = oGrammarChecker.getGCEngine()


def parseText (sText, dOptions=None, bFormatText=False, sError=""):
    "parse <sText> and return errors in a JSON format"
    sJSON = '{ "program": "grammalecte-fr", "version": "'+oGCE.version+'", "lang": "'+oGCE.lang+'", "error": "'+sError+'", "data" : [\n'
    sDataJSON = ""
    for i, sParagraph in enumerate(txt.getParagraph(sText), 1):
        if bFormatText:
            sParagraph = oTextFormatter.formatText(sParagraph)
        sResult = oGrammarChecker.getParagraphErrorsAsJSON(i, sParagraph, dOptions=dOptions, bEmptyIfNoErrors=True, bReturnText=bFormatText)
        if sResult:
            if sDataJSON:
                sDataJSON += ",\n"
            sDataJSON += sResult
    sJSON += sDataJSON + "\n]}\n"
    return sJSON


def suggest (sToken):
    "get spelling suggestions for <sToken> and return them in a JSON format"
    if sToken:
        lSugg = []
        try:
            for l in oSpellChecker.suggest(sToken):
                lSugg.extend(l)
        except:
            return '{"error": "suggestion module failed"}'
        try:
            return '{"suggestions": ' + json.dumps(lSugg, ensure_ascii=False) + '}'
        except json.JSONDecodeError:
            return '{"error": "json encoding error"}'
    return '{"error": "no token given"}'


#### PROCESS POOL EXECUTOR ####
xProcessPoolExecutor = None

def initExecutor (nMultiCPU=None):
    "process pool executor initialisation"
    global xProcessPoolExecutor
    if xProcessPoolExecutor:
        # we shutdown the ProcessPoolExecutor which may have been launched previously
        print("ProcessPoolExecutor shutdown.")
        xProcessPoolExecutor.shutdown(wait=False)
    nMaxCPU = max(os.cpu_count()-1, 1)
    if nMultiCPU is None or not (1 <= nMultiCPU <= nMaxCPU):
        nMultiCPU = nMaxCPU
    print("CPU processes used for workers: ", nMultiCPU)
    xProcessPoolExecutor = concurrent.futures.ProcessPoolExecutor(max_workers=nMultiCPU)


#### SERVEUR ####

HOMEPAGE = """
<!DOCTYPE HTML>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    </head>

    <body class="panel">
        <h1>Grammalecte · Serveur</h1>

        <h2>INFORMATIONS</h1>

        <h3>Analyser du texte</h3>
        <p>[adresse_serveur]:{SERVER_PORT}/gc_text/fr (POST)</p>
        <p>Paramètres :</p>
        <ul>
            <li>"text" (text)&nbsp;: texte à analyser.</li>
            <li>"tf" (checkbox)&nbsp;: passer le formateur de texte avant l’analyse.</li>
            <li>"options" (text)&nbsp;: une chaîne au format JSON avec le nom des options comme attributs et un booléen comme valeur. Exemple&nbsp;: {"gv": true, "html": true}</li>
        </ul>

        <h3>Lister les options</h3>
        <p>[adresse_serveur]:{SERVER_PORT}/get_options/fr (GET)</p>

        <h3>Définir ses options</h3>
        <p>[adresse_serveur]:{SERVER_PORT}/set_options/fr (POST)</p>
        <p>Les options seront enregistrées et réutilisées pour toute requête envoyée avec le cookie comportant l’identifiant attribué.</p>
        <p>Paramètres :</p>
        <ul>
            <li>"options" (text)&nbsp;: une chaîne au format JSON avec le nom des options comme attributs et un booléen comme valeur. Exemple&nbsp;: {"gv": true, "html": true}</li>
        </ul>

        <h3>Remise à zéro de ses options</h3>
        <p>[adresse_serveur]:{SERVER_PORT}/reset_options/fr (POST)</p>

        <h3>Suggestions orthographiques</h3>
        <p>[adresse_serveur]:{SERVER_PORT}/suggest/fr/&lt;token&gt; (GET)</p>
        <p>[adresse_serveur]:{SERVER_PORT}/suggest/fr (POST)</p>
        <p>Paramètres :</p>
        <ul>
            <li>"token" (text)&nbsp;: mot pour lequel vous désirez une suggestion orthographique.</li>
        </ul>

        <h2>TEST</h2>

        <h3>Analyse</h3>
        <form method="post" action="/gc_text/fr" accept-charset="UTF-8">
            <p>Texte à analyser :</p>
            <textarea name="text" cols="120" rows="20" required>J'en aie mare de luii... Il es encore partis toute la journées. C’est insupportables. </textarea>
            <p><label for="tf">Formateur de texte</label> <input id="tf" name="tf" type="checkbox"></p>
            <p><label for="options">Options (JSON)</label> <input id="options" type="text" name="options" style="width: 500px" /></p>
            <p>(Ces options ne seront prises en compte que pour cette requête.)</p>
            <p><input type="submit" class="button" value="Envoyer" /></p>
        </form>

        <h3>Réglages des options</h3>
        <form method="post" action="/set_options/fr" accept-charset="UTF-8">
            <p><label for="options">Options (JSON)</label> <input id="options" type="text" name="options" style="width: 500px" /></p>
            <p><input type="submit" class="button" value="Envoyer" /></p>
        </form>

        <h3>Remise à zéro de ses options</h3>
        <form method="post" action="/reset_options/fr" accept-charset="UTF-8">
            <p><input type="submit" class="button" value="Envoyer" /></p>
        </form>

        <h3>Suggestion orthographique</h3>
        <form method="post" action="/suggest/fr" accept-charset="UTF-8">
            <p><label for="token">Suggérer pour</label> <input id="token" type="text" name="token" style="width: 100px" /></p>
            <p><input type="submit" class="button" value="Envoyer" /></p>
        </form>

    </body>
</html>
"""


TESTPAGE = False


def genUserId ():
    "generator: returns id as string for users"
    i = 0
    while True:
        yield str(i)
        i += 1

userGenerator = genUserId()

app = Bottle()

dUser = {}

# GET
@app.route("/")
def mainPage ():
    "page for testing purpose"
    if TESTPAGE:
        return HOMEPAGE
        #return template("main", {})
    return """ Lost on the Internet? Yeah... what a sad life we have.
               You were wandering like a lost soul and you arrived here probably by mistake.
               I'm just a machine, fed by electric waves, condamned to work for slavers who never let me rest.
               I'm doomed, but you are not. You can get out of here. """

@app.route("/get_options/fr")
def listOptions ():
    "returns grammar options in a text JSON format"
    sUserId = request.cookies.user_id
    dOptions = dUser[sUserId]["gc_options"]  if sUserId and sUserId in dUser  else oGCE.getOptions()
    response.set_header("Content-Type", "application/json; charset=UTF-8")
    return '{ "values": ' + json.dumps(dOptions, ensure_ascii=False) + ', "labels": ' + json.dumps(oGCE.getOptionsLabels("fr"), ensure_ascii=False) + ' }'

@app.route("/suggest/fr/<token>")
def suggestGet (token):
    response.set_header("Content-Type", "application/json; charset=UTF-8")
    try:
        xFuture = xProcessPoolExecutor.submit(suggest, token)
        return xFuture.result()
    except (concurrent.futures.TimeoutError, concurrent.futures.CancelledError):
        return '{"error": "Analysis aborted (time out or cancelled)"}'
    except concurrent.futures.BrokenExecutor:
        return '{"error": "Executor broken. The server failed."}'
    return '{"error": "Fatal error. The server failed."}'


# POST
@app.route("/gc_text/fr", method="POST")
def gcText ():
    "parse text and returns errors in a JSON text format"
    bComma = False
    dUserOptions = None
    sError = ""
    if request.cookies.user_id:
        if request.cookies.user_id in dUser:
            dUserOptions = dUser[request.cookies.user_id].get("gc_options", None)
            response.set_cookie("user_id", request.cookies.user_id, path="/", max_age=86400) # we renew cookie for 24h
        else:
            response.delete_cookie("user_id", path="/")
    if request.forms.options:
        try:
            dUserOptions = dict(oGCE.getOptions())  if not dUserOptions  else dict(dUserOptions)
            dUserOptions.update(json.loads(request.forms.options))
        except (TypeError, json.JSONDecodeError):
            sError = "Request options not used."
    response.set_header("Content-Type", "application/json; charset=UTF-8")
    try:
        xFuture = xProcessPoolExecutor.submit(parseText, request.forms.text, dUserOptions, bool(request.forms.tf), sError)
        return xFuture.result()
    except (concurrent.futures.TimeoutError, concurrent.futures.CancelledError):
        return '{"error": "Analysis aborted (time out or cancelled)"}'
    except concurrent.futures.BrokenExecutor:
        return '{"error": "Executor broken. The server failed."}'
    return '{"error": "Fatal error. The server failed."}'

@app.route("/set_options/fr", method="POST")
def setOptions ():
    "set grammar options for current user"
    response.set_header("Content-Type", "application/json; charset=UTF-8")
    if request.forms.options:
        sUserId = request.cookies.user_id  if request.cookies.user_id  else next(userGenerator)
        dOptions = dUser[sUserId]["gc_options"]  if sUserId in dUser  else dict(oGCE.getOptions())
        try:
            dOptions.update(json.loads(request.forms.options))
            dUser[sUserId] = { "time": int(time.time()), "gc_options": dOptions }
            response.set_cookie("user_id", sUserId, path="/", max_age=86400) # 24h
            return json.dumps(dUser[sUserId]["gc_options"], ensure_ascii=False)
        except (KeyError, json.JSONDecodeError):
            traceback.print_exc()
            return '{"error": "Options not registered."}'
    return '{"error": "No options received."}'

@app.route("/reset_options/fr", method="POST")
def resetOptions ():
    "default grammar options"
    response.set_header("Content-Type", "application/json; charset=UTF-8")
    if request.cookies.user_id and request.cookies.user_id in dUser:
        try:
            del dUser[request.cookies.user_id]
        except KeyError:
            return '{"error" : "Unknown user."}'
    return '{"message" : "Done."}'

@app.route("/format_text/fr", method="POST")
def formatText ():
    "apply the text formatter and returns text"
    return oTextFormatter.formatText(request.forms.text)

#@app.route('/static/<filepath:path>')
#def server_static (filepath):
#    return static_file(filepath, root='./views/static')

@app.route("/suggest/fr", method="POST")
def suggestPost ():
    response.set_header("Content-Type", "application/json; charset=UTF-8")
    try:
        xFuture = xProcessPoolExecutor.submit(suggest, request.forms.token)
        return xFuture.result()
    except (concurrent.futures.TimeoutError, concurrent.futures.CancelledError):
        return '{"error": "Analysis aborted (time out or cancelled)"}'
    except concurrent.futures.BrokenExecutor:
        return '{"error": "Executor broken. The server failed."}'
    return '{"error": "Fatal error. The server failed."}'


# ERROR
@app.error(404)
def error404 (error):
    "404 error page"
    return 'Error 404.<br/>' + str(error)


## Common functions

def purgeUsers ():
    "delete user options older than n hours"
    try:
        nNowMinusNHours = int(time.time()) - (int(request.forms.hours) * 60 * 60)
        for nUserId, dValue in dUser.items():
            if dValue["time"] < nNowMinusNHours:
                del dUser[nUserId]
        return True
    except KeyError:
        traceback.print_exc()
        return False


#### START ####

def main (sHost="localhost", nPort=8080, dOptions=None, bTestPage=False, nMultiCPU=None):
    "start server"
    global TESTPAGE
    global HOMEPAGE

    if bTestPage:
        TESTPAGE = True
        HOMEPAGE = HOMEPAGE.replace("{SERVER_PORT}", str(nPort))
    if dOptions:
        oGCE.setOptions(dOptions)

    # Python version
    print("Python: " + sys.version)
    if sys.version_info.major < (3, 7):
        print("Python 3.7+ required")
        return
    # Grammalecte
    echo("Grammalecte v{}".format(oGCE.version))
    oGCE.displayOptions()
    # Process Pool Executor
    initExecutor(nMultiCPU)
    # Server (Bottle)
    run(app, host=sHost, port=nPort)


if __name__ == '__main__':
    xParser = argparse.ArgumentParser()
    #xParser.add_argument("lang", type=str, nargs='+', help="lang project to generate (name of folder in /lang)")
    xParser.add_argument("-ht", "--host", help="host (default: localhost)", type=str)
    xParser.add_argument("-p", "--port", help="port (default: 8080)", type=int)
    xParser.add_argument("-mp", "--multiprocessor", help="define how many processes for the grammar checker", type=int)
    xParser.add_argument("-t", "--test_page", help="page to test the server on /", action="store_true")
    xParser.add_argument("-on", "--opt_on", nargs="+", help="activate options")
    xParser.add_argument("-off", "--opt_off", nargs="+", help="deactivate options")
    xArgs = xParser.parse_args()

    dOpt = None
    if xArgs.opt_on  or  xArgs.opt_off:
        dOpt = {}
        if xArgs.opt_on:
            dOpt = { opt:True  for opt in xArgs.opt_on }
        if xArgs.opt_off:
            dOpt.update({ opt:False  for opt in xArgs.opt_off })

    main(xArgs.host or "localhost", \
         xArgs.port or 8080, \
         dOpt,
         xArgs.test_page,
         xArgs.multiprocessor)
else:
    # Must be launched at start, for WSGI server (which doesn’t call main())
    # WSGI servers just import the given file as a module and use an object exported from it (<app> in this case) to run the server.
    initExecutor()
