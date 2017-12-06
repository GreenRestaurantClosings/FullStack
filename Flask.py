import random
from flask import Flask, request, Response, json
app = Flask(__name__, static_url_path='')

# set DEBUG so you can see errors in your console
app.config['DEBUG'] = True

@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/query', methods=['POST'])
def query():
	body = request.get_json()
	query = body.get('query')
	data = json.dumps(autocomplete(query))
	return Response(data, status=200, mimetype='application/json')

if __name__ == '__main__':
	app.run()