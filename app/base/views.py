from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from InstaLiveCLI import InstaLiveCLI
import json
from app.utils import start_broadcast, stop_broadcast
base = Blueprint('base', __name__)

@base.route('/')
def login_route():

    try:
        settings = session['settings']
        print('got settings')
        return redirect(url_for('base.info_route'))

    except:
        return render_template('pages/login.html')

@base.route('/dashboard')
def info_route():

    try:
        settings = session['settings']
    except:
        return redirect(url_for('base.login_route'))

    print('> Update Broadcast Status')
    live = InstaLiveCLI(auth=session['settings'])
    session['settings']['data_stream']['status'] = live.get_broadcast_status()
    
    return render_template(
        'pages/dashboard.html',
        data_stream=session['settings']['data_stream'],
        is_muted=session['comments_muted'])

@base.route('/dashboard/refresh_key')
def refresh_handle():
    print('> Refreshing Stream Key')
    live = InstaLiveCLI(auth=session['settings'])
    live.create_broadcast()
    session['settings'] = live.settings
    
    return redirect(url_for('base.info_route'))

@base.route('/dashboard/logout')
def logout_handle():
    session.pop('settings',None)
    
    return redirect(url_for('base.login_route'))

@base.route('/login', methods=['POST'])
def login_handle():
    live = InstaLiveCLI(username=request.form['username'],password=request.form['password'])
    print('> Login to Instagram Server')
    login_status = live.login()

    if login_status:
        print('- Login Success')

        print('> Creating Broadcast')
        live.create_broadcast()

        print(live.settings)
        print('> Saving Cookies')

        # Init Session
        session['comments_muted'] = False
        session['settings'] = live.settings

        return redirect(url_for('base.info_route'))

    
    flash('Username or Password incorrect!')

    return redirect(url_for('base.login_route'))

@base.route('/start_broadcast')
def start():
    if start_broadcast():
        return {"status":"running","message":"You're live!!"}, 200
    else:
        return {"status":"error","message":"You're not live, start broadcast after you set the server key"}, 403

@base.route('/stop_broadcast')
def stop():
    if stop_broadcast():
        return {"status":"stopped","message":"The broadcast is ended"}, 200
    else:
        return {"status":"error","message":"something wrong here"}, 403