from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from InstaLiveCLI import InstaLiveCLI
import json
from app.utils import verified_retinad, get_session_setting, CurrentInstaSession
from .forms import LoginUserForm

base = Blueprint('base', __name__)

@base.route('/')
def login_route():
    form = LoginUserForm()
    try:
        if session['isLoggedIn'] == True:
            return redirect(url_for('base.info_route'))
        if session['verification_needed'] == True:
            return redirect(url_for('base.verification_sms_view'))
    except:
        pass


    return render_template('pages/login.html', form=form)

@base.route('/dashboard')
def info_route():
    try:
        if session['isLoggedIn'] == False:
            return redirect(url_for('base.login_route'))
    except:
        pass

    print('> Update Broadcast Status')

    current_instance = CurrentInstaSession()
    current_instance.load_settings()

    settings = current_instance.settings
    settings['data_stream']['status'] = current_instance.get_broadcast_status()
    
    print(settings['data_stream'])
    return render_template(
        'pages/dashboard.html',
        data_stream=settings['data_stream'],
        is_muted=session['comments_muted'])

@base.route('/dashboard/refresh_key')
def refresh_handle():
    print('> Refreshing Stream Key')

    current_instance = CurrentInstaSession()
    current_instance.load_settings()

    current_instance.create_broadcast()
    session['settings'] = current_instance.settings
    
    return redirect(url_for('base.info_route'))

@base.route('/dashboard/logout')
def logout_handle():
    session.pop('settings', None)
    session['isLoggedIn'] = False
    return redirect(url_for('base.login_route'))

@base.route('/login', methods=['POST'])
def login_handle():
    # Check to retinad first
    if verified_retinad(request.form['username']):
        print('> Login to Instagram Server')

        current_instance = CurrentInstaSession()
        login_status = current_instance.login(username=request.form['username'],password=request.form['password'])
        session['comments_muted'] = False
        session['username'] = request.form['username']
        if login_status:
            print('- Login Success')
            print('> Saving Cookies')

            
            print('> Creating Broadcast')
            current_instance.create_broadcast()

            # Init Session
            session['settings'] = current_instance.settings
            session['isLoggedIn'] = True

            return redirect(url_for('base.info_route'))

        if current_instance.two_factor_required:
            print('- Verification Required')
            session['settings'] = current_instance.settings
            session['verification_needed'] = True
            return redirect(url_for('base.verification_sms_view'))
        flash(current_instance.ig.LastJson['message'])

        return redirect(url_for('base.login_route'))
    
    flash('Username is not found in RETINAD server!')
    return redirect(url_for('base.login_route'))

@base.route('/verification')
def verification_sms_view():
    try:
        if session['isLoggedIn'] == True:
            return redirect(url_for('base.info_route'))
    except:
        pass

    current_instance = CurrentInstaSession()
    current_instance.load_settings()
    print(session['settings'])
    try:
        last_digit = current_instance.get_last_digit_phone()
        session['settings'] = current_instance.settings
    except Exception as e:
        print(e)
        flash('Please Log In')
        return redirect(url_for('base.login_route'))
    return render_template('pages/verification.html',last_digit=last_digit)

@base.route('/verification/send', methods=['POST'])
def verif_vode():
    code = request.get_json()['code']
    session['settings']['username'] = session['username']
    current_instance = CurrentInstaSession()
    current_instance.load_settings()
    
    try:
        result = current_instance.send_verification(code)
    except AttributeError:
        print('verification failed')
        flash('Verification Failed, Please Log In')
        session.pop('settings',None)
        return redirect(url_for('base.login_route'))
    if result:
        current_instance.ig.isLoggedIn = True
        print(current_instance.settings)
        print('> Creating Broadcast')
        current_instance.create_broadcast()

        session['settings'] = current_instance.settings
        session['isLoggedIn'] = True
        session['verification_needed'] = False
        return {
            'verified': result,
            },200
    return {
        'message':current_instance.ig.LastJson['message'],
        'verified': result,
        },200

@base.route('/start_broadcast')
def start():
    current_instance = CurrentInstaSession()
    current_instance.load_settings()

    if current_instance.start_broadcast():
        return {"status":"running","message":"You're live!!"}, 200
    else:
        return {"status":"error","message":"You're not live, start broadcast after you set the server key"}, 403

@base.route('/stop_broadcast')
def stop():
    current_instance = CurrentInstaSession()
    current_instance.load_settings()

    if current_instance.stop_broadcast():
        return {"status":"stopped","message":"The broadcast is ended"}, 200
    else:
        return {"status":"error","message":"something wrong here"}, 403