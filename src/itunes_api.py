#!/usr/bin/env python

from bottle import Bottle,  run
import sys, subprocess
from osascript import osascript, sudo


BASE= "itunes"
VERSION = "1.0"
URI="/api/%s/%s" % ( VERSION, BASE)

app = Bottle()

@app.route("/")
@app.route(URI + "/status")
def status():
    output = {"status": "stopped", "track": "", "artist" : ""}
    try:
        state = osascript('tell application "iTunes" to player state as string')                
        if state == "playing" or state == "paused" :
            artist = osascript('tell application "iTunes" to artist of current track as string');
            track = osascript('tell application "iTunes" to name of current track as string');
            album = osascript('tell application "iTunes" to get album of the current track as string');
            time = osascript('tell application "iTunes" to get time of the current track as string');
            playlist = osascript('tell application "iTunes" to get the name of current playlist as string')
            output["track"] = track
            output["artist"] = artist
            output["album"] = album
            output["time"] = time
            output["playlist"] = playlist
            output["status"] = state
    except:
        pass

    return output

@app.route(URI + "/play")
def play():
    try:
        state = osascript('tell application "iTunes" to play')
        return status()
    except:
        pass
    return {}

@app.route(URI + "/pause")
def pause():
    try:
        state = osascript('tell application "iTunes" to pause')
        return status()
    except:
        pass
    return {}

@app.route(URI + "/next")
def next():
    try:
        state = osascript('tell application "iTunes" to next track')
        return status()
    except:
        pass
    return {}

@app.route(URI + "/prev")
def prev():
    try:
        state = osascript('tell application "iTunes" to previous track')
        return status()
    except:
        pass
    return {}

@app.route(URI + "/mute")
def mute():
    try:
        state = osascript('tell application "iTunes" to set mute to true')
    except:
        pass
    return {}

@app.route(URI + "/unmute")
def unmute():
    try:
        state = osascript('tell application "iTunes" to set mute to false')
    except:
        pass
    return {}

@app.route(URI + "/vol")
@app.route(URI + "/volume")
@app.route(URI + "/vol/<level>")
@app.route(URI + "/volume/<level>")
def volume_level(level=""):
    try:
        vol = osascript('tell application "iTunes" to sound volume as integer')
        if level == "up":
            newvol = int(vol) + 10
        elif level == "down":
            newvol = int(vol) - 10
        elif level > 0 :
            newvol = level
        else:
            newvol = vol
        osascript("tell application \"iTunes\" to set sound volume to %s" % newvol);
        vol = osascript('tell application "iTunes" to sound volume as integer')
    except:
        pass
    return {"volume": vol}

@app.route(URI + "/stop")
def stop():
    try:
        state = osascript('tell application "iTunes" to stop')
        return status()
    except:
        pass
    return {}

@app.route(URI + "/quit")
def quit():
    try:
        state = osascript('tell application "iTunes" to quit')
    except:
        pass
    return {}

@app.route(URI + "/playlist")
@app.route(URI + "/playlist/<name>")
def playlist(name=""):
    try:
        if name:
            plylist_change_cmd = """
            tell application "iTunes"
            set new_playlist to "%s" as string
            play playlist new_playlist
            end tell
            """ % name                    
            osascript(plylist_change_cmd)        
        playlist = osascript('tell application "iTunes" to get name of every playlist');        
        return {"playlist": [ i.strip() for i in playlist.split(",")]}
    except:
        pass
    return {}

@app.route(URI + "/tracks")
@app.route(URI + "/tracks/<track>")
def tracks(track = ""):
    try:
        if track:
            track_cmd = """
            tell application "iTunes"
            set new_playlist to "%s" as string
            get name of every track in playlist new_playlist
            end tell 
            """ % track
            track = osascript(track_cmd)
            return {"tracks" : [ i.strip() for i in track.split(",") ] }

        track = osascript('tell application "iTunes" to get name of every track in current playlist')

        return {"tracks" : [ i.strip() for i in track.split(",") ] }
          
    except Exception as e:
        print e
        pass
    return {} 

@app.route(URI + "/changetracks")
@app.route(URI + "/changetracks/<playlist>")
@app.route(URI + "/changetracks/<playlist>/<track>")
def tracks(track = "", playlist = ""):
    try:
        if playlist and not track :
            track_cmd = """
            tell application "iTunes"
            set new_playlist to "%s" as string
            get name of every track in playlist new_playlist
            end tell 
            """ % playlist
            track = osascript(track_cmd)
            return {"tracks" : [ i.strip() for i in track.split(",") ] }

        if track and playlist:
            track_cmd = """
            tell application "iTunes"
            play track "%s" of playlist "%s"
            end tell
            """ % (track, playlist)
            osascript(track_cmd)
            return status()
        
            
        playlist = osascript('tell application "iTunes" to get name of every playlist');        
        return {"playlist" : [ i.strip() for i in playlist.split(",") ] }
          
    except:
        pass
    return {} 


#osascript -e 'tell app "itunes" to {duration, start, finish} of current track & {player position}'
@app.route(URI + "/shuf")
def shuf():
    try:
        state = osascript('tell application "iTunes" to set shuffle of current playlist to 1')
    except:
        pass
    return {}

@app.route(URI + "/nosh")
def nosh():
    try:
        state = osascript('tell application "iTunes" to set shuffle of current playlist to 0')
    except:
        pass
    return {}


class StripPathMiddleware(object):
  def __init__(self, app):
    self.app = app
  def __call__(self, e, h):
    e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
    return self.app(e,h)


myapp = StripPathMiddleware(app)    
run(app, host='0.0.0.0', port=8080, reloader=True)
