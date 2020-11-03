from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from InstaLiveCLI import InstaLiveCLI
import json
from app.utils import CurrentInstaSession

api = Blueprint('api', __name__)

@api.route('/live/viewers')
def home():
    current_instance = CurrentInstaSession()
    current_instance.load_settings()

    viewers = current_instance.get_viewers()
    return {
        'count':len(viewers),
        'list_viewers':viewers
        },200

@api.route('/live/comments')
def comments():
    current_instance = CurrentInstaSession()
    current_instance.load_settings()

    comments = current_instance.get_comments()
    return {
        'comments':comments,
        },200

@api.route('/live/comments/<msg>')
def send_comment_view(msg):
    current_instance = CurrentInstaSession()
    current_instance.load_settings()

    send_comment = current_instance.send_comments(msg)
    return {
        'commentSent':str(send_comment),
        },200


@api.route('/live/mute', methods=['GET', 'POST'])
def muted_comments():
    current_instance = CurrentInstaSession()
    current_instance.load_settings()

    is_muted = request.json['muted']
    send_comment = current_instance.toggle_mute_comments(is_muted)

    session['comments_muted'] = bool(not is_muted)
    return {
        'is_muted':not is_muted,
        },200
