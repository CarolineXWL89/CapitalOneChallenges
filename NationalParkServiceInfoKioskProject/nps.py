from flask import Flask, render_template, url_for, flash, redirect
import requests
import json

app = Flask(__name__)

#might turn into dictionary w/ State vs State code
state_list = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 
'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii','Idaho', 
'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 
'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 
'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 
'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
'West Virginia', 'Wisconsin', 'Wyoming']

state_code_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 
'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
'MA', 'MI', 'MN', 'MP', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 
'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 
'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

state_dict = [
	{'Alabama': 'AK'}, {'Alaska': 'AL'}, {'American Samoa': 'AS'}, {'Arizona':
	'AZ'}, {'Arkansas': 'AR'}, {'California': 'CA'}, {'Colorado': 'CO'}, 
	{'Connecticut': 'CT'}, {'Delaware': 'DE'}, {'District of Columbia': 'DC'},
	{'Florida': 'FL'}, {'Georgia': 'GA'}, {'Guam': 'GU'}, {'Hawaii': 'HI'},
	{'Idaho': 'ID'}, {'Illinois': 'IL'}, {'Indiana': 'IN'}, {'Iowa': 'IA'},
	{'Kansas': 'KS'}, {'Kentucky': 'KY'}, {'Louisiana': 'LA'}, {'Maine': 'ME'},
	{'Maryland': 'MD'}, {'Massachusetts': 'MA'}, {'Michigan': 'MI'}, {'Minnesota'
	: 'MN'}, {'Mississippi': 'MP'}, {'Missouri': 'MO'}, {'Montana': 'MT'}, 
	{'Nebraska': 'NE'}, {'Nevada': 'NV'}, {'New Hampshire': 'NH'}, {'New Jersey':
	'NJ'}, {'New Mexico': 'NM'}, {'New York': 'NY'}, {'North Carolina': 'NC'}, 
	{'North Dakota': 'ND'}, {'Ohio': 'OH'}, {'Oklahoma': 'OK'}, {'Oregon': 'OR'},
	{'Pennsylvania': 'PA'}, {'Rhode Island': 'RI'}, {'South Carolina': 'SC'}, 
	{'South Dakota': 'SD'}, {'Tennessee': 'TN'}, {'Texas': 'TX'}, {'Utah': 'UT'},
	{'Vermont': 'VT'}, {'Virginia': 'VA'}, {'Washington': 'WA'}, {'West Virginia'
	: 'WV'}, {'Wisconsin': 'WI'}, {'Wyoming': 'WY'}
]

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
	return render_template('states.html', title='Search By State', states=state_list)

#park search by state page
@app.route("/park_by_state")
def park_by_state():
	#sample api call; we want it to be variable; gotten from user input
	dud_api_request = api_params.get('api_base_call') + api_params.get('call_tags').get(7) + '?' + api_params.get('params').get(2) + 'WY&' + api_params.get('params').get(3) + '50' + '&api_key=' + api_params.get('api_key')
	r = requests.get(dud_api_request)
	#gets info from api call
	list_of_parks = json.loads(r.text)['data'] 
	num_parks = json.loads(r.text)['total']
	#return dud_api_request;
	return render_template('parks.html', title='Parks in State Selected', num_parks=num_parks, list_of_parks=list_of_parks)

#news page
@app.route("/news")
def news():
	return render_template('general_layout.html', title='News in Parks')

#run w/o command line instructions
#__name__ is __main__ if run w/ python.script directly; i.e. will enter conditional
#if imported somewhere else, __name__ will be name of that module
if __name__ == '__main__':
	app.run(debug=True)