import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify

from analyse_sound import *
# from .CV.eye_tracker import *

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv', 'wmv'}


UPLOAD_DIR = "uploads"

# Create the file system
if not os.path.isdir(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        valid_username = "testuser"
        valid_password = "AIPentaHack"

        if username == valid_username and password == valid_password:
            session['username'] = username
            return redirect(url_for("upload"))
        else:
            flash("Invalid username or password.", category="error")

    return render_template("signin.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if 'username' not in session:
        flash("Please log in to access this page.", category="error")
        return redirect(url_for("signin"))

    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part.", category="error")
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash("No selected file.", category="error")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['video_file'] = filename
            flash("Video uploaded successfully!", category="success")

    return render_template("upload.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/analyse", methods=["GET", "POST"])
def analyse():
    if 'username' not in session:
        flash("Please log in to access this page.", category="error")
        return redirect(url_for("signin"))

    file = ""
    if request.method == "GET":
        file = session['video_file']

        if file == '':
            flash("No selected file.", category="error")
            return redirect(request.url)
        
        preds, interps = analyse_audio(file)

        preds_str = list(map(lambda x: id2label[x], preds))

        session["preds_str"] = preds_str
        session["interps"] = interps
        session['curr_pred'] = preds_str[0]
        session['curr_interps'] = interps[0]

    return render_template("upload.html")

@app.route('/slider_update', methods=['POST', 'GET'])
def slider():
    if request.method == "POST":
        received_data = request.get_json()
        idx = int(received_data['idx'])
        print(idx, session["preds_str"])
        curr_pred = session["preds_str"][idx]
        curr_interps = session["interps"][idx]
        
        print(curr_pred, curr_interps)
        body = {
            "pred": curr_pred,
            "data": curr_interps
        }
        return jsonify(body)
        # return body


@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("Logged out successfully.", category="success")
    return redirect(url_for("signin"))

if __name__ == "__main__":
    app.run(debug=True)

