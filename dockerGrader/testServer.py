
from flask import Flask
import dockerUtil
from celery import Celery
from celery.utils.log import get_task_logger

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend = app.config['CELERY_RESULT_BACKEND'],
        broker = app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
logger = get_task_logger(__name__)

celery = make_celery(flask_app)

@celery.task
def runDocker(project, netId):
    grader = dockerGrader(project, netId, logger)
    grader.dockerRun()

@flask_app.route('/')
def index():
    return "index"

@flask_app.route('/json/<project>/<netId>')
def gradingJson(project, netId):
    result = runDocker.delay(project, netId)
    return "Done"
