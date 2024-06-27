from flask import Flask
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create a StreamHandler for outputting to the console
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO)
# Optional: Format the log messages
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(console_handler)

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
