import pickle
from flask import session
from InstaLiveCLI import InstaLiveCLI
import requests

from config import Config

class CurrentInstaSession:
    def __init__(self):
        self.ig = None
    
    def load_settings():
        self.ig = InstaLiveCLI(auth=session['settings'])
    def start_broadcast(self):
        print('> Starting Broadcast')
        return self.ig.start_broadcast()

    def stop_broadcast(self):
        print('> Stopping Broadcast')
        return self.ig.end_broadcast()
    
    def get_viewers(self):
        print("> Getting Viewers")
        user, id = self.ig.get_viewer_list()
        return user
    
    def get_comments(self):
        print("> Getting Comments")
        return self.ig.get_comments()

    def send_comments(self,text):
        print("> Sending Comments :"+text)
        return self.ig.send_comment(text)

    def toggle_mute_comments(self,mute):
        if mute:
            print("> Unmute Comments")
            return self.ig.unmute_comment()
        else:
            print("> Mute Comments")
            return self.ig.mute_comments()

    def send_verification(self,code):
        return self.ig.two_factor(code)

def verified_retinad(username):
    response = requests.get(Config.RETINAD_API_URL).json()
    return response['username'] == username