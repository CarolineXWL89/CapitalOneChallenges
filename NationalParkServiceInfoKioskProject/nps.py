from flask import Flask, render_template, url_for, flash, redirect
import requests
import json

app = Flask(__name__)

#might turn into dictionary w/ State vs State code
state_list = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii','Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

state_code_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MP', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

state_dict = {
	'Alabama': 'AK', 'Alaska': 'AL', 'Arizona':'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE','Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI','Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA','Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MP', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey':'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR','Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT','Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}


api_params = {
	'api_key': 'Gyfs3mI6dUX4pKpcjcfevIVBLS5H8nytwe6L5Yue',
	'api_base_call': 'https://developer.nps.gov/api/v1/',
	'call_tags': {
		1: 'alerts', 
		2: 'articles', 
		3: 'campgrounds', 
		4: 'events', 
		5: 'lessonplans',
		6: 'newsreleases', 
		7: 'parks', 
		8: 'people', 
		9: 'places', 
		10: 'visitorcenters'},
	'params': {
		1: 'parkCode=', #array[String] query
		2: 'stateCode=', #array[String] query
		3: 'limit=', #integer query
		4: 'start=', #integer query
		5: 'q=', #String query
		6: 'fields=', #array[String] query
		7: 'sort=' #array[String] query
	}
}

#home page
@app.route("/")
@app.route("/home")
def home():
	#return 'Hello World!'
	return render_template('home.html', title='Home')

#about page
@app.route("/about")
def about():
	#return 'About World!'
	return render_template('about.html', title='About')

#states page
@app.route("/states")
def states_list():
	return render_template('states.html', title='Search By State', states=state_dict, api_params=api_params)

#parks page TBD TESTING
#state = "CA"#request.args.get('type')
@app.route('/parks_in_<state_abb>_<state_full>', methods=['GET', 'POST'])
#@app.route('/parks/<state>', methods=['GET', 'POST'])
def parks(state_abb, state_full):
	#trial api call; should search for state that we clicked
	trial_api_request = api_params.get('api_base_call') + api_params.get('call_tags').get(7) + '?' + api_params.get('params').get(2) + state_abb + '&' + api_params.get('params').get(3) + '50' + '&api_key=' + api_params.get('api_key')
	#print(trial_api_request)
	r = requests.get(trial_api_request)
	#print("api request from " + state + ": %s" % (r != None))
	#gets info from api call
	list_of_parks = json.loads(r.text)['data'] 
	#print("list of parks: " + ', '.join(list_of_parks))
	num_parks = json.loads(r.text)['total']
	#print("number of parks: " + num_parks)
	#return api request formatted hopefully
	return render_template('parks.html', title='Parks in ' + state_full, num_parks=num_parks, list_of_parks=list_of_parks, state_abb=state_abb, state_full=state_full)

@app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>", methods=['GET', 'POST'])
def chosen_park(state_abb, state_full, park_name, park_code):
	
	#parks? API request
	call_tag = api_params.get('call_tags').get(7)
	#print(call_tag)
	parks_api_request = generate_api_call(call_tag, park_code, state_abb)
	#print(parks_api_request)
	r_parks = requests.get(parks_api_request)
	single_park_list = json.loads(r_parks.text)['data']

	#alerts? API request
	call_tag = api_params.get('call_tags').get(1)
	alerts_api_request = generate_api_call(call_tag, park_code, state_abb)
	r_alerts = requests.get(alerts_api_request)
	num_alerts = json.loads(r_alerts.text)['total']
	list_of_alerts = json.loads(r_alerts.text)['data']

	#campgrounds? API request
	call_tag = api_params.get('call_tags').get(3)
	campgrounds_api_request = generate_api_call(call_tag, park_code, state_abb)
	r_campgrounds = requests.get(campgrounds_api_request)
	num_campgrounds = json.loads(r_campgrounds.text)['total']
	list_of_campgrounds = json.loads(r_campgrounds.text)['data']

	#news? API request
	call_tag = api_params.get('call_tags').get(6)
	news_api_request = generate_api_call(call_tag, park_code, state_abb)
	r_news = requests.get(news_api_request)
	num_news = json.loads(r_news.text)['total']
	list_of_news = json.loads(r_news.text)['data']

	#events? API request
	call_tag = api_params.get('call_tags').get(4)
	events_api_request = generate_api_call(call_tag, park_code, state_abb)
	r_events = requests.get(events_api_request)
	num_events = json.loads(r_events.text)['total']
	list_of_events = json.loads(r_events.text)['data']

	#articles? API request
	call_tag = api_params.get('call_tags').get(2)
	articles_api_request = generate_api_call(call_tag, park_code, state_abb)
	r_articles = requests.get(articles_api_request)
	num_articles = json.loads(r_articles.text)['total']
	list_of_articles = json.loads(r_articles.text)['data']

	#lessons? API request
	call_tag = api_params.get('call_tags').get(5)
	lessons_api_request = generate_api_call(call_tag, park_code, state_abb)
	r_lessons = requests.get(lessons_api_request)
	num_lessons = json.loads(r_lessons.text)['total']
	list_of_lessons = json.loads(r_lessons.text)['data']

	#people? API request
	call_tag = api_params.get('call_tags').get(8)
	people_api_request = generate_api_call(call_tag, park_code, state_abb)
	r_people = requests.get(people_api_request)
	num_people = json.loads(r_people.text)['total']
	list_of_people = json.loads(r_people.text)['data']

	#places? API request
	call_tag = api_params.get('call_tags').get(9)
	places_api_request = generate_api_call(call_tag, park_code, state_abb)
	r_places = requests.get(places_api_request)
	num_places = json.loads(r_places.text)['total']
	list_of_places = json.loads(r_places.text)['data']

	return render_template('park_layout.html', state_abb=state_abb, state_full=state_full, park=single_park_list, num_alerts=num_alerts, alerts=list_of_alerts, num_camps=num_campgrounds,campgrounds=list_of_campgrounds, api_params=api_params, num_news=num_news, news=list_of_news, num_articles=num_articles, articles=list_of_articles, num_events=num_events, events=list_of_events, num_lessons=num_lessons, lessons=list_of_lessons, num_people=num_people, people=list_of_people, num_places=num_places, places=list_of_places)

def generate_api_call(call_tag, park_code, state_code, start=0, q="", fields=[], sort=[], limit=50):
	api_call = api_params.get('api_base_call') + call_tag + '?'
	if park_code:
		api_call += api_params.get('params').get(1) + park_code + '&'
	if state_code:
		api_call += api_params.get('params').get(2) + state_code + '&'
	api_call += api_params.get('params').get(3) + str(limit) + '&'
	if start:
		api_call += api_params.get('params').get(4) + str(start) + '&'
	if q:
		api_call += api_params.get('params').get(5) + q + '&'
	if fields:
		api_call += api_params.get('params').get(6) + '%2C%20'.join(fields) + '&'
	if sort:
		api_call += api_params.get('params').get(7) + '%2C%20'.join(sort) + '&'
	api_call += 'api_key=' + api_params.get('api_key')
	return api_call

@app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>/<alert_type>_<alert_num>", methods=['GET', 'POST'])
def display_alert(state_abb, state_full, park_name, park_code, alert_type, alert_num):
	alerts_api_request = generate_api_call('alerts', park_code, state_abb)
	#print(alerts_api_request)
	r = requests.get(alerts_api_request)
	list_of_alerts = json.loads(r.text)['data']
	alert = list_of_alerts[int(alert_num)]
	alert_title = alert.get('title')
	alert_desc = alert.get('description')
	return render_template('single_alert.html', title=park_name + ' Alerts',state_abb=state_abb, park_name=park_name, alert_title=alert_title, alert_desc=alert_desc, alert_type=alert_type)

@app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>/alerts", methods=['GET', 'POST'])
def display_all_alerts(state_abb, state_full, park_name, park_code):
	alerts_api_request = generate_api_call('alerts', park_code, state_abb)
	r = requests.get(alerts_api_request)
	list_of_alerts = json.loads(r.text)['data']
	return render_template('alerts.html', title=park_name + ' ' + alert_type +' Alert', park_name=park_name, alerts=list_of_alerts)

@app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>/<campground_name>")
#@app.route('/campground_dummy_link')
def show_campground(state_abb, state_full, park_name, park_code, campground_name):#, index):
	campgrounds_api_request = generate_api_call('campgrounds', park_code, state_abb)
	print(campgrounds_api_request)
	r = requests.get(campgrounds_api_request)
	list_of_campgrounds = json.loads(r.text)['data']
	campground = None
	for i in range(len(list_of_campgrounds)):
		if list_of_campgrounds[i].get('name') == campground_name:
			campground = list_of_campgrounds[i]
			break
	if campground == None:
		print("Campground not found")
		sys.exit(1)
	return render_template('campground_layout.html', title=campground_name,state_abb=state_abb, state_full=state_full, park_name=park_name, campground_name=campground_name, campground=campground)
	#return render_template('campground_layout.html', title='Dummy Campground')

@app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>/<campground_name>/<campsite_name>")
def show_campsite(state_abb, state_full, park_name, park_code, campground_name, campsite_name):
	#TODO
	return render_template('campsite.html')

#REMOVE TENTATIVELY
#park search by state page dud tester
@app.route("/park_by_state")
def park_by_state():
	#sample api call; we want it to be variable; gotten from user input
	dud_api_request = api_params.get('api_base_call') + api_params.get('call_tags').get(7) + '?' + api_params.get('params').get(2) + 'WY&' + api_params.get('params').get(3) + '50' + '&api_key=' + api_params.get('api_key')
	print(dud_api_request)
	r = requests.get(dud_api_request)
	print("api request from WY dud: " + ": %s" % (r != None))
	#gets info from api call
	list_of_parks = json.loads(r.text)['data'] 
	num_parks = json.loads(r.text)['total']
	print("number of parks: " + num_parks)
	#return dud_api_request;
	return render_template('parks.html', title='Parks in State Selected', num_parks=num_parks, list_of_parks=list_of_parks, state="WY")

#REMOVE TENTATIVELY
#news page (general? Might replace later)
@app.route("/news")
def news():

	return render_template('general_layout.html', title='News in Parks')

# @app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>/<news_title>", methods=['GET', 'POST'])
# def news_by_park(state_abb, state_full, park_name, park_code, news_title):
# 	#TODO
# 	return render_template("single_news.html", state_abb=state_abb, state_full=state_full, park_name=park_name, park_code=park_code, new_single=news)

#might delete the single display pages b/c directly linked to page
#CURRENTLY: keep campgrounds, events erroring, lessons not set + erroring, 
@app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>/news/")
def display_all_news(state_abb, state_full, park_name, park_code):
	#TODO
	return render_template("news.html", state_abb=state_abb, state_full=state_full, park_name=park_name, park_code=park_code, news_all=news_all)

@app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>/<article_id>/")
def article_by_park(state_abb, state_full, park_name, park_code, article_id):
	#TODO	
	return render_template('single_article.html', state_abb=state_abb, state_full=state_full, park_name=park_name, park_code=park_code, article=article)

@app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>/articles/")
def display_all_articles(state_abb, state_full, park_name, park_code):
	#TODO
	return render_template('articles.html', state_abb=state_abb, state_full=state_full, park_name=park_name, park_code=park_code, articles=articles)

@app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>/<event_id>/")
def event_by_park(state_abb, state_full, park_name, park_code, event_id):
	#TODO
	return render_template('single_event.html', state_abb=state_abb, state_full=state_full, park_name=park_name, park_code=park_code, event=event)

@app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>/events/")
def display_all_events(state_abb, state_full, park_name, park_code):
	#TODO
	return render_template('events.html', state_abb=state_abb, state_full=state_full, park_name=park_name, park_code=park_code, events=events)

@app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>/<lesson_id>")
def lesson_by_park(state_abb, state_full, park_name, park_code, lesson_id):
	#TODO
	return render_template('single_lesson.html', state_abb=state_abb, state_full=state_full, park_name=park_name, park_code=park_code, lesson=lesson)

@app.route("/parks_in_<state_abb>_<state_full>/<park_name>_<park_code>/lessons/")
def display_all_lessons(state_abb, state_full, park_name, park_code):
	#TODO
	return render_template('lessons.html', state_abb=state_abb, state_full=state_full, park_name=park_name, park_code=park_code, lessons=lessons)

#run w/o command line instructions
#__name__ is __main__ if run w/ python.script directly; i.e. will enter conditional
#if imported somewhere else, __name__ will be name of that module
if __name__ == '__main__':
	app.run(debug=True)