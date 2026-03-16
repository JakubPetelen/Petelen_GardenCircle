# backend/main.py
from flask import Flask
from dotenv import load_dotenv
import os
from .database import close_db
from .models import ensure_schema

# Load environment variables from .env file
load_dotenv()

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_STATIC_DIR = os.path.join(_PROJECT_ROOT, "static")
_TEMPLATES_DIR = os.path.join(_PROJECT_ROOT, "templates")

app = Flask(__name__, static_folder=_STATIC_DIR, template_folder=_TEMPLATES_DIR)


@app.route("/")
def root():
    from .routes import render_template
    return render_template("home.html")


def create_app():
    # Defer imports to avoid circulars during setup
    from .routes import register_routes
    register_routes(app)
    app.teardown_appcontext(close_db)
    # Initialize DB schema inside app context
    with app.app_context():
        ensure_schema()
    return app


if __name__ == "__main__":
    create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
