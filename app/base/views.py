from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from InstaLiveCLI import InstaLiveCLI
import json
from app.utils import start_broadcast, stop_broadcast, verified_retinad
from .forms import LoginUserForm

base = Blueprint('base', __name__)

login = None

@base.route('/')
def login_route():
    form = LoginUserForm()
    try:
        settings = session['settings']
        print('got settings')
        return redirect(url_for('base.info_route'))
    except:
        return render_template('pages/login.html', form=form)

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
    # Check to retinad first
    if verified_retinad(request.form['username']):
        global login
        login = InstaLiveCLI(username=request.form['username'],password=request.form['password'])
        print('> Login to Instagram Server')
        login_status = login.login()
        session['comments_muted'] = False
        if login_status:
            print('- Login Success')

            print('> Creating Broadcast')
            login.create_broadcast()

            print('> Saving Cookies')

            # Init Session
            session['settings'] = login.settings

            return redirect(url_for('base.info_route'))

        if login.two_factor_required:
            session['settings'] = login.settings
            return redirect(url_for('base.verification_sms_view'))
        flash('Username or Password incorrect!')

        return redirect(url_for('base.login_route'))
    
    flash('Username is not valid from RETINAD server!')
    return redirect(url_for('base.login_route'))

@base.route('/verification')
def verification_sms_view():
    form = LoginUserForm()
    return render_template('pages/verification.html', form=form)

@base.route('/verification/send', methods=['POST'])
def verif_vode():
    code = request.get_json()['code']
    result = login.two_factor(code)

    if result:
        login.isLoggedIn = True
        

        print('> Creating Broadcast')
        login.create_broadcast()

        session['settings'] = login.settings
    return {
        'verified': result,
        },200

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