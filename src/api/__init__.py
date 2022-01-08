from flask import Flask

from src.api.controller.index_routes import blueprint as index_blueprint
from src.api.controller.inference_routes import blueprint as inference_blueprint


app = Flask(__name__)
app.register_blueprint(index_blueprint)
app.register_blueprint(inference_blueprint)

if __name__ == "__main__":
    app.run()
