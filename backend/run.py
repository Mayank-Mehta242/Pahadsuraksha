import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    # Runs on port 8000 to match the Vite dev-server proxy in
    # frontend/vite.config.js (server.proxy["/api"].target).
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
