import os
from flask import Flask, redirect, request, session, url_for, jsonify, render_template
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
from routes import userManagement as dbUser
from routes import character_generation as dbChar

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = os.urandom(24)
app.config["MAX_CONTENT_LENGTH"] = 80 * 1024 * 1024
app.config["MAX_FORM_MEMORY_SIZE"] = 80 * 1024 * 1024
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
    if not session.get("user_id"):
        return redirect("/index.html")
    return render_template("mainmenu.html")


@app.route("/character-creation")
def character_creation():
    if not session.get("user_id"):
        return redirect("/index.html")
    characters = dbChar.view_characters()
    pending_roll = session.get("pending_roll")
    return render_template(
        "character_creation.html", characters=characters, pending_roll=pending_roll
    )


@app.route("/api/roll-preview", methods=["POST"])
def api_roll_preview():
    if not session.get("user_id"):
        return redirect("/index.html")
    roll = dbChar.preview_roll()
    return jsonify(roll)



@app.route("/api/create-character", methods=["POST"])
def api_create_character():
    if not session.get("user_id"):
        return redirect("/index.html")
    data = request.form
    name = data.get("name", "").strip()
    roll = session.pop("pending_roll", None)
    if not name or not roll:
        return redirect("/character-creation")
    pfp_data = data.get("pfp", "")
    ALLOWED_PREFIXES = (
        "data:image/png;",
        "data:image/jpeg;",
        "data:image/gif;",
        "data:image/webp;",
    )
    MAX_B64_LEN = 80 * 1024 * 1024
    if pfp_data and not pfp_data.startswith(ALLOWED_PREFIXES):
        return redirect("/character-creation")
    if pfp_data and len(pfp_data) > MAX_B64_LEN:
        return redirect("/character-creation")
    character_id = dbChar.insert_character(
        name, roll["species_id"], roll["attributes"], pfp_data or None
    )
    if character_id is None:
        session["pending_roll"] = roll
        return redirect("/character-creation")
    return redirect("/character-creation")


@app.route("/api/rename-character", methods=["POST"])
def api_rename_character():
    if not session.get("user_id"):
        return redirect("/index.html")
    data = request.form
    character_id = data.get("character_id")
    new_name = data.get("name", "").strip()
    if not character_id or not new_name:
        return (
            render_template("character_creation.html", error="Missing required field"),
            400,
        )
    result = dbChar.rename_character(character_id, new_name)
    if result == "not_found":
        return (
            render_template("character_creation.html", error="Character not found"),
            404,
        )
    if result == "duplicate":
        return (
            render_template(
                "character_creation.html", error="A character already has this name"
            ),
            409,
        )
    if result != "success":
        return render_template("character_creation.html", error="Invalid input"), 400
    return redirect("/character-creation")


@app.route("/api/edit-pfp", methods=["POST"])
def api_edit_pfp():
    if not session.get("user_id"):
        return redirect("/index.html")
    data = request.get_json(silent=True) or {}
    character_id = data.get("character_id")
    new_pfp = data.get("profile_image")
    if not character_id or not new_pfp:
        return jsonify({"error": "Missing required fields"}), 400
    ALLOWED_PREFIXES = (
        "data:image/png;",
        "data:image/jpeg;",
        "data:image/gif;",
        "data:image/webp;",
    )
    MAX_B64_LEN = 80 * 1024 * 1024
    if not new_pfp.startswith(ALLOWED_PREFIXES):
        return jsonify({"error": "Invalid image format"}), 400
    if len(new_pfp) > MAX_B64_LEN:
        return jsonify({"error": "Image too large. Maximum size is 31MB."}), 413
    result = dbChar.edit_pfp(new_pfp, character_id)
    if result != "success":
        return jsonify({"error": "Something went wrong"}), 400
    return jsonify({"profile_image": new_pfp}), 200


@app.route("/api/delete-character", methods=["POST"])
def api_delete_character():
    if not session.get("user_id"):
        return redirect("/index.html")
    data = request.form
    character_id = data.get("character_id")
    if not character_id:
        return render_template("character_creation.html", error="Invalid character"), 400
    result = dbChar.delete_character(character_id)
    if result != "success":
        return render_template("character_creation.html", error="Something went wrong."), 404
    return redirect("/character-creation")


@app.route("/gauntlet")
def gauntlet():
    if not session.get("user_id"):
        return redirect("/index.html")
    return render_template("gauntlet.html")

@app.route("/gauntlet_endless")
def gauntlet_endless():
    if not session.get("user_id"):
        return redirect("/index.html")
    characters = dbChar.view_characters()
    return render_template("gauntlet_endless.html", characters=characters)

@app.route("/gauntlet_waves")
def gauntlet_waves():
    if not session.get("user_id"):
        return redirect("/index.html")
    character_selected = bool(session.get("selected_character_id"))
    if character_selected:
        return render_template("gauntlet_waves.html", characters=[], character_selected=True)
    characters = dbChar.view_characters()
    return render_template("gauntlet_waves.html", characters=characters, character_selected=False)

@app.route("/api/select-character", methods=["POST"])
def api_select_character():
    if not session.get("user_id"):
        return redirect("/index.html")
    character_id = request.form.get("character_id")
    if not character_id:
        return redirect("/gauntlet_waves")
    session["selected_character_id"] = int(character_id)
    return redirect("/gauntlet_waves")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)