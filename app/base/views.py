from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from InstaLiveCLI import InstaLiveCLI
import json
from app.utils import verified_retinad, get_session_setting
from app.api.views import CurrentInstaLive
from .forms import LoginUserForm

base = Blueprint('base', __name__)

@base.route('/')
def login_route():
    form = LoginUserForm()
    try:
        if CurrentInstaLive.isLoggedIn == True:
            return redirect(url_for('base.info_route'))
    except:
        pass
    return render_template('pages/login.html', form=form)

@base.route('/dashboard')
def info_route():
    try:
        if CurrentInstaLive.isLoggedIn == False:
            return redirect(url_for('base.login_route'))
    except:
        return redirect(url_for('base.login_route'))

    print('> Update Broadcast Status')

    settings = CurrentInstaLive.settings
    settings['data_stream']['status'] = CurrentInstaLive.get_broadcast_status()
    
    print(settings['data_stream'])
    return render_template(
        'pages/dashboard.html',
        data_stream=settings['data_stream'],
        is_muted=session['comments_muted'])

@base.route('/dashboard/refresh_key')
def refresh_handle():
    print('> Refreshing Stream Key')

    CurrentInstaLive.create_broadcast()
    session['settings'] = CurrentInstaLive.settings
    
    return redirect(url_for('base.info_route'))

@base.route('/dashboard/logout')
def logout_handle():
    session.pop('settings',None)
    
    return redirect(url_for('base.login_route'))

@base.route('/login', methods=['POST'])
def login_handle():
    # Check to retinad first
    if verified_retinad(request.form['username']):
        print('> Login to Instagram Server')
        login_status = CurrentInstaLive.login(username=request.form['username'],password=request.form['password'])

        session['comments_muted'] = False
        if login_status:
            print('- Login Success')
            print('> Saving Cookies')

            # Init Session

            # session['settings'] = CurrentInstaLive.settings
            # CurrentInstaLive.load_settings()

            print('> Creating Broadcast')
            CurrentInstaLive.create_broadcast()

            return redirect(url_for('base.info_route'))

        if CurrentInstaLive.two_factor_required:
            # session['settings'] = CurrentInstaLive.settings
            return redirect(url_for('base.verification_sms_view'))
        flash('Username or Password incorrect!')

        return redirect(url_for('base.login_route'))
    
    flash('Username is not found in RETINAD server!')
    return redirect(url_for('base.login_route'))

@base.route('/verification')
def verification_sms_view():
    try:
        if CurrentInstaLive.isLoggedIn == True:
            return redirect(url_for('base.info_route'))
    except:
        return redirect(url_for('base.login_route'))

    try:
        last_digit = CurrentInstaLive.get_last_digit_phone()
    except Exception as e:
        print(e)
        flash('Please Log In')
        return redirect(url_for('base.login_route'))
    return render_template('pages/verification.html',last_digit=last_digit)

@base.route('/verification/send', methods=['POST'])
def verif_vode():
    code = request.get_json()['code']

    try:
        result = CurrentInstaLive.send_verification(code)
    except AttributeError:
        flash('Verification Failed, Please Log In')
        session.pop('settings',None)
        return redirect(url_for('base.login_route'))
    if result:
        CurrentInstaLive.ig.isLoggedIn = True
        print(CurrentInstaLive.settings)
        print('> Creating Broadcast')
        CurrentInstaLive.create_broadcast()

        session['settings'] = CurrentInstaLive.settings
        # CurrentInstaLive.load_settings()
    return {
        'verified': result,
        },200

@base.route('/start_broadcast')
def start():
    if CurrentInstaLive.start_broadcast():
        return {"status":"running","message":"You're live!!"}, 200
    else:
        return {"status":"error","message":"You're not live, start broadcast after you set the server key"}, 403

@base.route('/stop_broadcast')
def stop():
    if CurrentInstaLive.stop_broadcast():
        return {"status":"stopped","message":"The broadcast is ended"}, 200
    else:
        return {"status":"error","message":"something wrong here"}, 403