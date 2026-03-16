import os

# Ensure relative paths resolve from project root when running on Vercel.
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.main import create_app  # noqa: E402

app = create_app()

