#!/bin/python3
import re
import ignition
from bottle import redirect, route, static_file, response, run
import subprocess

rooturl = "//"

@route("/")
def index():
    return ""

@route("/api/v1/check")
def check():
    response.content_type = "text/plain"
    response.headers['Access-Control-Allow-Origin'] = '*'
    return "OK"

@route("/api/v1/<url:re:.+>")
def defr(url):
    req = ignition.request(rooturl+url.replace("$", "?"))
    response.headers['Access-Control-Allow-Origin'] = '*'
    if ".jpg" in url or ".png" in url or "favicon.txt" in url:
        response.headers["Cache-Control"] = "public, max-age=604800"
    images = [".jpg", ".png", ".gif", ".ico"]
    for i in images:
        if i in str(req.url):
            response.content_type = "image/"+str(req.url.split(".")[1:][1])
    if str(req).split(" ")[0].startswith("1"):
        return "$$$input$$$"+str(req).split("\n")[0].replace(str(req).split("\n")[0].split(" ")[0], "")
    else:
        if str(req).split(" ")[0].startswith("5") or str(req).split(" ")[0].startswith("0") or str(req).split(" ")[0].startswith("4"):
            return "# Error "+str(req).split("\n")[0].split(" ")[0]+"\n"+str(req).split("\n")[0].replace(str(req).split("\n")[0].split(" ")[0], "")
        else:
            if not str(req.raw_body) == "":
                return req.raw_body
            else:
                redirect("/get/"+url+"/")

@route("/api/v1/gitid")
def gitid():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.content_type = "text/plain"
    return str(subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])).replace("b'", "").replace("\\n'", "")

run(host="127.0.0.1", port=1970, server="tornado")
