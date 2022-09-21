import os
import logging
from logging.handlers import RotatingFileHandler
from engine_api import app


if not app.debug:
    # if app.debug:
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/engine_api.log", maxBytes=10240 * 1024, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
