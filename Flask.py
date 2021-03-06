import random
from flask import Flask, request, Response, json
import pyrebase
import numpy as np
from sklearn import linear_model

app = Flask(__name__, static_url_path='/static')

# set DEBUG to see errors in console
app.config['DEBUG'] = True

restaurants = []
logisticData = []


config = {}
with open("configs.txt") as configs:
        data = json.load(configs)
        config = data["config"]

firebase = pyrebase.initialize_app(config)
db = firebase.database()
#pull data from firebase under 'Restaurants'
restaurant_names = db.child("Restaurants").get()
for rest in restaurant_names.each():
	#pull data from firebase, append to list
    logisticData.append(rest.val())

"""a = np.zeros((len(logisticData), 4))"""
a = np.zeros((len(logisticData), 6))
b = np.zeros((len(logisticData), 1))

for element in range(len(logisticData)):
    #setting initial values to -1 ensures that data points WITHOUT any of these attributes (a gap in data) do not skew the regression relation.
    #a value of -1 ensures that these points are seen as completely extraneous, and thus the regression relation is unaffected by them.
    TAnumReviews = -1
    TARating = -1
    YelpRating = -1
    YNumReviews = -1
    AvgHealthScore = -1
    NumReports = -1
    if("Closed" in logisticData[element] and logisticData[element]["Closed"]):
        b[element] = 1
        #sets the vector element = 1, which corresponds to CLOSED
    if("Trip Advisor Number of Reviews" in logisticData[element]):
        #TA reviews was stored in the format "# reviews"
        temp = logisticData[element]["Trip Advisor Number of Reviews"].split(" ")
        TAnumReviews = int(temp[0])
    if("Trip Advisor Rating" in logisticData[element]):
        #TA rating was stored in the format "# bubbles out of 5 bubbles". Words were separated at the space :)
        temp2 = logisticData[element]["Trip Advisor Rating"].split(" ")
        TARating = float(temp2[0])
    if("Yelp Rating" in logisticData[element]):
        #Yelp rating was stored as a float
        YelpRating = logisticData[element]["Yelp Rating"]
    if("YelpNumReviews" in logisticData[element]):
        #Yelp NumReviews was stored as an int
        YNumReviews = logisticData[element]["YelpNumReviews"]
    if("Average Report Score" in logisticData[element]):
        #Average score of all Health Inspections is stored as a float
        AvgHealthScore = logisticData[element]["Average Report Score"]
    if("Number of Reports" in logisticData[element]):
        #Number of health inspections is stored as in int
        NumReports = logisticData[element]["Number of Reports"]

    a[element] = [TAnumReviews, TARating, YelpRating, YNumReviews, AvgHealthScore, NumReports]

logreg = linear_model.LogisticRegression()
logreg.fit(a, b)


for i in range(len(logisticData)):
    #print(logreg.predict_proba(a[i, :].reshape(1,-1)), logisticData[i]["Restaurant Name"])
    if (type(logisticData[i]["Restaurant Name"]) == str):
        score = logreg.predict_proba(a[i, :].reshape(1,-1))[0,1]
        restaurants.append({"name":logisticData[i]["Restaurant Name"], "score": "%.2f%%" % round(score*100, 2)})


def takeScore(elem):
	return elem["score"]

#sort elements in array [name, score]
restaurants = sorted(restaurants, key=takeScore, reverse = True)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/aboutUs')
def aboutUs():
    return app.send_static_file('aboutUs.html')

@app.route('/query', methods=['POST'])
def query():
	body = request.get_json(force = True)
	query = body["query"]
	submitted = body["submitted"]
	data = None
	#if enter key pressed
	if submitted:
		data = json.dumps(search(query) + autocomplete(query))
	#while typing
	else:
		data = json.dumps(autocomplete(query))
	return Response(data, status=200, mimetype='application/json')


#autocomplete function on searchbar while typing
def autocomplete(query):
	result = []
	for options in restaurants:
		# separate all query words and option restaurant names.
		query_words = query.upper().split()
		option_words = options["name"].upper().split()
		# if query is longer than option then skip the option
		if len(query_words) > len(option_words):
			continue

		# loop through the query words and break if no option is found.
		for idx in range(len(query_words)):
			if not (option_words[0].startswith(query_words[0])):
				break
			if idx != 0 and not prefixOfWord(query_words[idx], option_words[1:]):
				break
		else:
			result.append(options)
	return result

def prefixOfWord(word, options):
	# Loop through all the words in options
	for option in options:
		if option.startswith(word):
			#if prefix is found in one
			return True
	return False


#results that appear after pressing 'enter'
def search(query):
	result = []
	#loop through each dictionary in restaurants list
	for options in restaurants:
		#if length of query is longer than restaurant name
		if len(query) < len(options):
			break
		#create array of restaurant names
		separate = options["name"].split("\n")
		#loop through restaurant names, append restaurants name and score if distance between name and query falls below threshold
		for word in separate:
			if substring_edit_distance(query.lower(), word) == True:
				result.append(options)
	return result


def substring_edit_distance(word1, word2):
	#for distance between strings
	threshold = 2
	for i in range(len(word2) - len(word1) + 1):
		#compare query to restaurant names, sliding window of length of query, true if difference between is less than 2
		if edit_distance(word1, word2[i:i + (len(word1))]) < threshold:
			return True
	return False


#levenshtein distance
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
	#return distance between the two strings
	return m[len(s1)][len(s2)]


if __name__ == '__main__':
    app.run()