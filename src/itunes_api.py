#!/usr/bin/env python

from bottle import Bottle,  run
import sys
from osascript import osascript, sudo
from iTunesController import iTunesController

itunes = iTunesController()

BASE= "itunes"
VERSION = "1.0"
URI="/api/%s/%s" % ( VERSION, BASE)

app = Bottle()

@app.route("/")
@app.route(URI + "/status")
def status():
    return itunes.status()

@app.route(URI + "/play")
def play():
    return itunes.play()

@app.route(URI + "/pause")
def pause():
    return itunes.pause()

@app.route(URI + "/next")
def next():
    return itunes.next()

@app.route(URI + "/prev")
def prev():
    return itunes.prev()

@app.route(URI + "/mute")
def mute():
    return itunes.mute()

@app.route(URI + "/unmute")
def unmute():
    return itunes.unmute()

@app.route(URI + "/stop")
def stop():
    return itunes.stop()

@app.route(URI + "/quit")
def quit():
    return itunes.quit()

@app.route(URI + "/shuf")
def shuf():
    return itunes.shuf()

@app.route(URI + "/nosh")
def nosh():
    return itunes.nosh()

@app.route(URI + "/vol")
@app.route(URI + "/volume")
@app.route(URI + "/vol/<level>")
@app.route(URI + "/volume/<level>")
def volume_level(level=""):
    return itunes.volume(level)

@app.route(URI + "/playlist")
@app.route(URI + "/playlist/<name>")
def playlist(name=""):
    return itunes.playlist(name) 

@app.route(URI + "/tracks")
@app.route(URI + "/tracks/<playlist>")
def tracks(playlist = ""):
    return itunes.tracks(playlist)

@app.route(URI + "/changetracks")
@app.route(URI + "/changetracks/<playlist>")
@app.route(URI + "/changetracks/<playlist>/<track>")
def changetracks(track = "", playlist = ""):
    return itunes.changetracks(track, playlist)              

class StripPathMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.app(e,h)


myapp = StripPathMiddleware(app)    
run(app, host='0.0.0.0', port=8080, reloader=True)
