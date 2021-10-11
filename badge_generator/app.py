import io
import os

from flask import (
    Flask, request, send_file
)

from badges import UsrBadge


app = Flask(__name__)

@app.route('/badge')
def badge():
    badge = UsrBadge()
    data, mimetype = badge.render(request.args)
    return send_file(io.BytesIO(data), mimetype=mimetype)

if __name__ == '__main__':
    app.run(
        port=7070, host=os.getenv('FLASK_BIND_IP', '0.0.0.0'),
        debug=True, use_reloader=True
    )