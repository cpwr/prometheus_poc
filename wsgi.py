from app import app
from prometheus_toolbox.expose.flask.setup import add_metrics_endpoint, setup_default_metrics

setup_default_metrics(app)
app = add_metrics_endpoint(app)

if __name__ == "__main__":
    app.run_simple()
