from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from InstaLiveCLI import InstaLiveCLI
import json
from app.utils import start_broadcast, stop_broadcast, get_viewers, get_comments, send_comments

api = Blueprint('api', __name__)

@api.route('/live/viewers')
def home():
    viewers = get_viewers()
    return {
        'count':len(viewers),
        'list_viewers':viewers
        },200

@api.route('/live/comments')
def comments():
    comments = get_comments()
    return {
        'comments':comments,
        },200

@api.route('/live/comments/<msg>')
def send_comment_view(msg):
    send_comment = send_comments(msg)
    return {
        'commentSent':str(send_comment),
        },200


@api.route('/live/mute')
def muted_comments():
    print(request.json)
    # send_comment = toggle_mute_comments()
    return {
        'commentSent':str(
            'tes'
        ),
        },200