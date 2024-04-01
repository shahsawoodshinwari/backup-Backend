import os
import threading

from .database import db
from flask import Flask, request, jsonify
from flask_cors import CORS
from .utils.extract_person import extract_person
from .utils.analyze_person import analyze_person
from .utils.extract_person_site_2 import extract_person_site_2
from .utils.analyze_person_site_2 import analyze_person_site_2
from .extensions.extensions import Migrate, JWTManager
from apscheduler.schedulers.background import BackgroundScheduler


def pulsse_app(config_file=os.path.join(os.path.dirname(__file__), "..", "config.py")):
    app = Flask(__name__)
    #app = Flask(__name__, static_folder='/home/ubuntu/Frontend/build', static_url_path='/')

    app.config.from_pyfile(config_file)
    cors = CORS(origins='*')
    cors.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    @app.route('/')
    def index():
        # return app.send_static_file('index.html')
        return "hello"
    
    @app.before_request
    def basic_authentication():
        headers = { 'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type' }
        if request.method == 'OPTIONS' or request.method == 'options':
            return jsonify(headers), 200

    from Pulsse.views.user_view import user_blueprint
    app.register_blueprint(user_blueprint)

    from Pulsse.views.customer_view import customer_blueprint
    app.register_blueprint(customer_blueprint)

    from Pulsse.views.visit_view import visit_blueprint
    app.register_blueprint(visit_blueprint)

    from Pulsse.views.generate_frames_view import frames_blueprint
    app.register_blueprint(frames_blueprint)

    from Pulsse.views.dashboard import dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)
    # =========================================== site 1 ================================================

    # thread1 = threading.Thread(target=extract_person, args=(1, app))
    # thread1.daemon = True
    # thread1.start()
    
    # Configure the scheduler
    # scheduler = BackgroundScheduler()
    # scheduler.start()
    # # Schedule the analyze_person function every 3 seconds
    # scheduler.add_job(analyze_person, 'interval', seconds=3, args=(1,))

    # =========================================== site 2 ================================================

    thread1 = threading.Thread(target=extract_person, args=(1, app))
    thread1.daemon = True
    thread2 = threading.Thread(target=extract_person_site_2, args=(2, app))
    thread2.daemon = True
    # thread1.start()
    # thread2.start()

    scheduler = BackgroundScheduler()
    scheduler.start()
    # Schedule the analyze_person function every 3 seconds
    # scheduler.add_job(analyze_person, 'interval', seconds=3, args=(1,))
    # scheduler.add_job(analyze_person_site_2, 'interval', seconds=3, args=(2,))
    
    # Configure the scheduler
    # scheduler2 = BackgroundScheduler()
    # scheduler2.start()
    # # Schedule the analyze_person function every 3 seconds
    # scheduler2.add_job(analyze_person_site_2, 'interval', seconds=3, args=(2,))

    # ==========================================================================================================
    return app


