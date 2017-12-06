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
    body = request.get_json(force = True)
    print(body)
    query = body["query"]
    submitted = body["submitted"]
    data = None
    if submitted == True:
        data = json.dumps(search(query))
    else:
        data = json.dumps(autocomplete(query))
    return Response(data, status=200, mimetype='application/json')

# Just a sample data set. Feel free to use something else!
config = {}
with open("configs.txt") as configs:
        data = json.load(configs)
        config = data["config"]
firebase = pyrebase.initialize_app(config)
db = firebase.database()
restaurant_names = db.child("Restaurants").get()
for rest in restaurant_names.each():
    restaurants.append(rest.val()["Restaurant Name"])



def getNames():
    # This picks a random element from the mixmaxFeatures array regardless of input
    # TODO Replace this with your autocomplete function
    result = []
    restaurant_names = db.child("Restaurants").get()
    for rest in restaurant_names.each():
        result.append(rest.val()["Restaurant Name"])
    return result

def autocomplete(query):
    print("autocomplete")
    result = []
    for options in restaurants:
	# Separate all query words and option words.
        query_words = query.upper().split()
        option_words = options.upper().split()

	# If query is longer than option then skip the option
        if len(query_words) > len(option_words):
            continue

	# Loop through the query words and break if no option is found.
        for idx in range(len(query_words)):
            if not (option_words[0].startswith(query_words[0])):
                break
                if idx != 0 and not prefixOfWord(query_words[idx], option_words[1:]):
                    break
        else:
            result.append(options)
    return result

def search(query):
    #threshold = 2
    result = []
    for options in restaurants:
        if len(query) > len(options):
            continue
        if substring_edit_distance(query.lower(), options.lower()) == True:
            result.append(options)
    return result

def substring_edit_distance(word1, word2):
    threshold = 2
    for i in range(len(word2) - len(word1) + 1):
        print(word2[i:i + (len(word1))])
        if edit_distance(word1, word2[i:i + (len(word1))]) < threshold:
            return True
    return False

def edit_distance(s1, s2):
    m = []
    m.append([0])

    for i in range(1, len(s1) + 1):
        m.append([i])

    for j in range(1, len(s2) + 1):
        m[0].append(j)

    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            m[i].append(min(m[i-1][j-1] if (s1[i-1] == s2[j-1]) else (m[i-1][j-1] + 1), m[i-1][j] + 1, m[i][j-1] + 1))

    return m[len(s1)][len(s2)]

'''
def ngrams(n, string):
    ngrams = set()
    start = 0
    end = start + n
    while end <= len(string):
        ngrams.add(string[start:end])
        start+=1
        end+=1
    return ngrams

#jaccard coefficient for n-grams of two words
def jaccard(n, string1, string2):
    ngram1 = ngrams(n, string1)
    ngram2 = ngrams(n, string2)

    intersection_size = len(ngram1 & ngram2)
    union_size = len(ngram1 | ngram2)

    return intersection_size / float(union_size)
'''

def prefixOfWord(word, options):
	# Loop through all the words in options
	# If prefix is found in one, return True
	for option in options:
		if option.startswith(word):
			return True
	return False

if __name__ == '__main__':
    app.run()