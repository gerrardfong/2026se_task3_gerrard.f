from flask import Flask, redirect, request, session, url_for, jsonify, render_template
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
from routes import userManagement as dbUser
from routes import character_generation as dbChar

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = b"_53oi3uriq9pifpff;apl"
csrf = CSRFProtect(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup.html", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("/signup.html")
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "").strip()
        if confirm_password == password:
            try:
                success = dbUser.insertUser(username, email, password)
                if success is True:
                    user_id = dbUser.loginUser(email, password)
                    session["user_id"] = user_id
                    return redirect("/mainmenu.html")
                else:
                    return render_template("/signup.html", error="Email already exists")
            except Exception:
                return render_template("/signup.html", error="Registration failed")
        else:
            return render_template("/signup.html", error="Passwords do not match")
    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html", login=False)
    if request.method == "POST":
        identity = request.form.get("identity", "").strip()
        password = request.form.get("password", "").strip()
        user_id = dbUser.loginUser(identity, password)
        if user_id:
            session["user_id"] = user_id
            return redirect("/mainmenu.html")
        else:
            return render_template("/index.html", error="Invalid Credentials")
        
@app.route("/mainmenu.html")
def mainmenu():
    return render_template("mainmenu.html"
    "")


@app.route("/character-creation")
def character_creation():
    characters = dbChar.view_characters()
    return render_template("character_creation.html", characters=characters)


@app.route("/api/roll-preview")
def api_roll_preview():
    result = dbChar.preview_roll()
    return jsonify(result)


@app.route("/api/create-character", methods=["POST"])
def api_create_character():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    species_id = data.get("species_id")
    attributes = data.get("attributes", {})
    if not name or not species_id or not attributes:
        return jsonify({"error": "Missing required fields"}), 400
    character_id = dbChar.insert_character(name, int(species_id), attributes)
    return jsonify({"character_id": character_id}), 201


@app.route("/gauntlet")
def gauntlet():
    return render_template("gauntlet.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)