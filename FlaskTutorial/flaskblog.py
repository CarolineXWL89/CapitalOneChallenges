from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__) #__name__ var name of module s.t. flask 
#knows where to look

#set secret key for keeping forms data secure; set as environment var later
#gen from command line
app.config['SECRET_KEY'] = '043c7950b9db3e91ed10047e9caef960'

#random data to post (part 2) in list of dictionaries
posts = [
	{
		'author': 'Caroline Liu',
		'title': 'Blog post 1',
		'content': 'first post content',
		'date_posted': '25 May 2019'
	},
	{
		'author': 'Felicity McGregor',
		'title': 'Blog post 2',
		'content': 'second post content',
		'date_posted': '25 May 2019'
	}
]

@app.route("/") #what we type into our browser
@app.route("/home")
#decorator allows us to display what we want given that ^^input
#into browser (handles backend stuff)
#normally home page
def home():
    #return "<h1>HOME PAGE</h1>"
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
	#return "<h1>About</h1>"
	return render_template('about.html', title='About')

#part 3: registration route
@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm() #will pass into registration template
	#will create register.html template; template will have access to form created
	if form.validate_on_submit():
		flash(f'Account created for { form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'dummy@gmail.com' and form.password.data == "12345":
			flash('You have been successfully logged in!', 'sucess')
			return redirect(url_for('home'))
		else:
			flash('Login unsuccessful. Please check username and password.', 'danger')
	return render_template('login.html', title='Login', form=form)


#run w/o command line instructions
#__name__ is __main__ if run w/ python.script directly; i.e. will enter conditional
#if imported somewhere else, __name__ will be name of that module
if __name__ == '__main__':
	app.run(debug=True)