from flask import Flask
from flask import render_template
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header

app = Flask(__name__, template_folder="2. PWA/templates")
app.secret_key = b"_53oi3uriq9pifpff;apl"
csrf = CSRFProtect(app)

@app.route("/")
def index():
    return render_template("/index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)