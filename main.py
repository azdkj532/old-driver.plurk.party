import os
import json

import bottle_pgsql
from bottle import Bottle, route, run, static_file, error, response

app = bottle.Bottle()
plugin = bottle_pgsql.Plugin(os.environ.get('DATABASE_URL', ''))
app.install(plugin)

@app.route('/')
@app.route('/static/<filename:path>')
def index(filename=None):
    if filename is None:
        filename = 'index.html'
    return static_file(filename, root='./static')

@app.route('/go')
def data(offset, db):
    try:
        offset = int(offset)
    except Exception:
        offset = 0
    row = db.execute('SELECT * FROM plurk LIMIT 50 OFFSET %s', (offset,))

    response.set_header('Content-Type', 'application/json')
    if row:
        return json.dumps(row)
    else:
        return []


@app.error(404)
def error404(error):
    return '<h1>車速過快 翻車了</h1>'

if os.environ.get('APP_LOCATION') == 'heroku':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    app.run(host='localhost', port=8080, debug=True)
