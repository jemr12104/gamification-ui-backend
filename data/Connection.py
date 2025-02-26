from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """Initialize the database configuration."""
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://flaskuser:1234@localhost/gamification"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 1800,  # Prevents MySQL timeout issues
        "pool_pre_ping": True,  # Ensures connection is alive before use
        "echo": False,  # Set to True for debugging queries
    }
    db.init_app(app)
