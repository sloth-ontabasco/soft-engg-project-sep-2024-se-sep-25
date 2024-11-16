from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api
import src.models
from src.config import CI, PORT, Config, LocalDevConfig
from src.setup import setup_api, setup_auth

app, api = None, None


def setup_app() -> Flask:
    app = Flask(__name__)
    cors = CORS(
        app=app,
        resources={r"/api/*": {"origins": "http://localhost:5173"}},
        supports_credentials=True,
    )
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["10000 per day", "1000 per hour"],
        storage_uri="memory://",
    )
    api = Api(app)

    if CI:
        app.config.from_object(Config)
    else:
        app.config.from_object(LocalDevConfig)

    setup_api(app, api)
    setup_auth(app)
    return app


app = setup_app()

if __name__ == "__main__":
    if CI:
        app.run(port=None, debug=False)
    else:
        app.run(port=8081, debug=True)
