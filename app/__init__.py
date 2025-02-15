import yaml
from flask import Flask
from app.extensions import csrf, db


def create_app() -> Flask:
    app = Flask(__name__)

    csrf.init_app(app=app)

    cred = yaml.load(
        open("./cred.yaml"),
        Loader=yaml.Loader,
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    host = cred["mysql_host"]
    user = cred["mysql_user"]
    password = cred["mysql_password"]
    db_name = cred["mysql_db"]

    # Issue with not being able to install mysqlclient, so I did pip install pymysql to fix this
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"

    # Registered db
    db.init_app(app=app)

    from app.app import bp as main_bp
    from app.routes.machines import machine_bp
    from app.routes.products import product_bp
    from app.routes.stock import stock_bp
    from app.routes.stock_records import record_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(machine_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(record_bp)

    return app
