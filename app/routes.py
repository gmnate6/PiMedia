from flask import current_app as app, send_from_directory, render_template, abort, redirect, url_for
import os
from .utils import *

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/movies")
def movies():
    movies = get_media_data_by_category("movies")
    return render_template("media_list.html", medias=movies)

@app.route("/shows")
def shows():
    shows = get_media_data_by_category("shows")
    return render_template("media_list.html", medias=shows)

@app.route('/play/<category>/<id>/<filename>')
def play(category, id, filename):
    data = get_media_data(category, id)
    data["filename"] = filename

    # Pass Episode List if Show
    episodes = get_episodes(category, id) if category == "shows" else []

    return render_template('player.html', data=data, episodes=episodes)

@app.route("/play/<category>/<id>/")
def play_redirect(category, id):
    path = validate_media_path(category, id)
    
    # Get mp4
    mp4_files = glob.glob(os.path.join(path, '*.mp4'))
    if not mp4_files:
        abort(404)
    filename = os.path.basename(mp4_files[0])

    # Redirect
    return redirect(url_for('play', category=category, id=id, filename=filename))

@app.route("/media/<category>/<id>/<filename>")
def media(category, id, filename):
    media_path = validate_media_path(category, id)
    check_media_file_exists(media_path, filename)

    return send_from_directory(media_path, filename)
