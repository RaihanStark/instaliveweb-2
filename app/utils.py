from flask import session
from InstaLiveCLI import InstaLiveCLI
import requests

from app.models import User
from app import db
from config import Config



class CurrentInstaSession:
    def __init__(self):
        self.ig = None
    
    def load_settings(self):
        print('load_settings')
        self.ig = InstaLiveCLI(auth=session['settings'])

    def login(self,username,password):
        self.ig = InstaLiveCLI(username=username,password=password)
        return self.ig.login()

    @property
    def settings(self):
        return self.ig.settings

    @property
    def two_factor_required(self):
        return self.ig.two_factor_required

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

    def get_broadcast_status(self):
        return self.ig.get_broadcast_status()

    def create_broadcast(self):
        return self.ig.create_broadcast()

    def get_last_digit_phone(self):
        return self.ig.two_factor_last_number

    def send_verification(self,code):
        return self.ig.two_factor(code)

    @property
    def isLoggedIn(self):
        return self.ig.isLoggedIn

def verified_retinad(username):
    response = requests.post(
        Config.RETINAD_API_URL, 
        headers={
            'Accept':'application/json'
        },json={
            'ig_account':username
        }).json()
    print(response)
    return response['boolean'] or Config.RETINAD_API_SKIP

def get_session_setting():
    return session['settings']

# Databases Stuff

def add_user_to_db(username,session):
    # if user doesn't exists
    if check_user_exists() == False:
        new_user = User(username=username,session=session)
        db.session.add(new_user)
        db.session.commit()
        return True
    else:
        return False

def check_user_exists(username):
    return User.query.filter_by(username=username).first() != None
