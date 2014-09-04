from osascript import osascript, sudo

class iTunesController(object):
    def __init__(self):
        self._get_itunes_state 			= 'tell application "iTunes" to player state as string'
        self._get_current_artist 		= 'tell application "iTunes" to artist of current track as string'
        self._get_current_track 		= 'tell application "iTunes" to name of current track as string'
        self._get_current_album 		= 'tell application "iTunes" to get album of the current track as string'
        self._get_current_time 			= 'tell application "iTunes" to get time of the current track as string'
        self._get_playlist 			= 'tell application "iTunes" to get the name of current playlist as string'
        self._set_itunes_state_to_play 	        = 'tell application "iTunes" to play'
        self._set_itunes_state_to_pause 	= 'tell application "iTunes" to pause'
        self._set_itunes_to_next_track 		= 'tell application "iTunes" to next track'
        self._set_itunes_to_previous_track 	= 'tell application "iTunes" to previous track'
        self._set_itunes_to_mute 		= 'tell application "iTunes" to set mute to true'
        self._set_itunes_to_unmute 		= 'tell application "iTunes" to set mute to false'
        self._get_itunes_volume 		= 'tell application "iTunes" to sound volume as integer'
        self._set_itunes_volume 		= 'tell application "iTunes" to set sound volume to %s'
        self._set_itunes_state_to_stop 		= 'tell application "iTunes" to stop'
        self._set_itunes_state_to_quit 		= 'tell application "iTunes" to quit'
        self._set_itunes_state_to_shuffle 	= 'tell application "iTunes" to set shuffle of current playlist to 1'
        self._set_itunes_state_to_noshuffle 	= 'tell application "iTunes" to set shuffle of current playlist to 0'
        self._get_all_playlist 			= 'tell application "iTunes" to get name of every playlist'
        self._get_track_of_current_playlist 	= 'tell application "iTunes" to get name of every track in current playlist'
        self._set_itunes_plylist 		= '''tell application "iTunes" 
                                                        set new_playlist to "%s" as string
                                                        play playlist new_playlist
                                                    end tell'''
        self._get_track_from_playlist 		= '''tell application "iTunes"
                                                        set new_playlist to "%s" as string
                                                        get name of every track in playlist new_playlist
                                                    end tell'''
        self._set_track_from_playlist 		= '''tell application "iTunes"
                                                        play track "%s" of playlist "%s"
                                                    end tell'''

    def exe_cmd(self, cmd):
        try:
            return osascript(cmd)
        except:
            return {}

    def status(self):
        output = {"status": "stopped", "track": "", "artist" : "", "album": "", "playlist": "", "time":""}
        state = self.exe_cmd(self._get_itunes_state) 
        if state == "playing" or state == "paused":
            output["track"] = self.exe_cmd(self._get_current_track)
            output["artist"] = self.exe_cmd(self._get_current_artist)
            output["album"] = self.exe_cmd(self._get_current_album)
            output["time"] = self.exe_cmd(self._get_current_time)
            output["playlist"] = self.exe_cmd(self._get_playlist)
            output["status"] = state

        return output    

    def next(self):
        self.exe_cmd(self._set_itunes_to_next_track)
        return self.status()

    def prev(self):
        self.exe_cmd(self._set_itunes_to_previous_track)
        return self.status()

    def play(self):
        self.exe_cmd(self._set_itunes_state_to_play)
        return self.status()

    def pause(self):
        self.exe_cmd(self._set_itunes_state_to_pause)
        return self.status()

    def stop(self):
        self.exe_cmd(self._set_itunes_state_to_stop)
        return self.status()

    def quit(self):
        self.exe_cmd(self._set_itunes_state_to_quit)
        return {}

    def mute(self):
        self.exe_cmd(self._set_itunes_to_mute)
        return {}

    def unmute(self):
        self.exe_cmd(self._set_itunes_to_unmute)
        return {}

    def shuf(self):
        self.exe_cmd(self._set_itunes_state_to_shuffle)
        return {}

    def nosh(self):
        self.exe_cmd(self._set_itunes_state_to_noshuffle)
        return {}    

    def volume(self, level):
        vol = self.exe_cmd(self._get_itunes_volume)        
        if level == "up":
            newvol = int(vol) + 10
        elif level == "down":
            newvol = int(vol) - 10
        elif level > 0 :
            newvol = level
        else:
            newvol = vol
        self.exe_cmd(self._set_itunes_volume % newvol)
        vol = self.exe_cmd(self._get_itunes_volume)    
        return {"volume": vol}

    def playlist(self, name):
        if name:
            self.exe_cmd(self._set_itunes_plylist % name)            

        playlist = self.exe_cmd(self._get_all_playlist)
        if playlist:
            return {"playlist": [ i.strip() for i in playlist.split(",")]}
        return {}

    def tracks(self, playlist):
        if playlist:
            track = self.exe_cmd(self._get_track_from_playlist % playlist)
            if track:
                return {"tracks" : [ i.strip() for i in track.split(",") ] }

        track = self.exe_cmd(self._get_track_of_current_playlist)
        if track:
            return {"tracks" : [ i.strip() for i in track.split(",") ] }
        return {}

    def changetracks(self, track, playlist):
        if playlist and not track :
            track = self.exe_cmd(self._get_track_from_playlist % playlist)
            if track:
                return {"tracks" : [ i.strip() for i in track.split(",") ] }

        if track and playlist:
            self.exe_cmd(self._set_track_from_playlist % (track, playlist))
            return self.status()


        playlist = self.exe_cmd(self._get_all_playlist)
        if playlist:
            return {"playlist" : [ i.strip() for i in playlist.split(",") ] }
        return {}
