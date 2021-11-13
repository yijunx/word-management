from flask import Flask
from flask.json import JSONEncoder
from flask_request_id_header.middleware import RequestID
from flask_cors import CORS
from app.util.app_logging import get_logger, init_logger
from app.config.app_config import conf
from datetime import datetime

# blueprints
from app.blueprints.word_private_api import bp as WordPublicBp
from app.blueprints.word_public_api import bp as WordPrivateBp

# from app.blueprints.user import bp as userBp
# from app.blueprints.internal import bp as internalBp


logger = get_logger(__name__)


app = Flask(__name__)
# app.secret_key = conf.APP_SECRET  # for the csrf to work
init_logger(app=app)

# CSRFProtect(app)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app.config["REQUEST_ID_UNIQUE_VALUE_PREFIX"] = ""
RequestID(app)
CORS(app, resources={r"/api/*": {"origins": conf.CORS_ALLOWED_ORIGINS.split(",")}})

app.json_encoder = CustomJSONEncoder


app.register_blueprint(WordPrivateBp)
app.register_blueprint(WordPublicBp)
# app.register_blueprint(internalBp)
