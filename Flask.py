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

def autocomplete(query):
	# This picks a random element from the mixmaxFeatures array regardless of input
	# TODO Replace this with your autocomplete function
	result = []
	for options in mixmax_features:
	# Separate all query words and option words.
		query_words = query.upper().split()
		option_words = options.upper().split()

	# If query is longer than option then skip the option
		if len(query_words) > len(option_words):
			continue
	
	# Loop through the query words and break if no option is found.
	for idx in range(len(query_words)):
		
		# Check first word, with first option word.
		if not (option_words[0].startswith(query_words[0])):
			break
	
		# Check rest of query words with option words.
		if idx != 0 and not prefixOfWord(query_words[idx], option_words[1:]):
			break
	else:
		result.append(options)
	return result

def prefixOfWord(word, options):
	# Loop through all the words in options
	# If prefix is found in one, return True
	for option in options:
		if option.startswith(word):
			return True
	return False
	
if __name__ == '__main__':
	app.run()