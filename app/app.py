from flask import Flask, render_template, request, Response
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from .robot import robot_blueprint
from .reqs import reqs_blueprint
from .navigator import rooms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

app.register_blueprint(robot_blueprint, url_prefix='/robot')
app.register_blueprint(reqs_blueprint, url_prefix='/request')

USERNAME = 'admin'
PASSWORD = 'cake'




@app.route('/')
def index():
    return render_template('index.html', rooms=rooms)

@app.route('/admin')
def admin():
    # Check if the request contains authorization headers
    auth = request.authorization
    if not auth or not (auth.username == USERNAME and auth.password == PASSWORD):
        # If the credentials are missing or incorrect, send a 401 Unauthorized response
        return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return render_template('admin.html', rooms=rooms)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)


