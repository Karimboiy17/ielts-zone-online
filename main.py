from dotenv import load_dotenv
load_dotenv()

import os
from asgiref.wsgi import WsgiToAsgi
from app import create_app

# Create Flask WSGI app
_flask_app = create_app()

# Expose ASGI-compatible app for Railway / uvicorn
app = WsgiToAsgi(_flask_app)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level="debug" if debug else "info"
    )
