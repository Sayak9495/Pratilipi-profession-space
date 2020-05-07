from flask import Flask, render_template, g, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'qweqweqsfdqwfsdsghjyujlmbnvou'


@app.before_request
def before_request():
	#get all infos from db here
	g.user = None
	if 'username' in session:
		g.user = "Sayak"

@app.route("/")
def index():
	return redirect(url_for('login'))

@app.route("/home")
def home():
	if not g.user:
		return redirect(url_for('login'))
	return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	if (request.method == 'POST'):
		session.pop('username', None)
		username = request.form['email']
		password = request.form['password']
		
		if(username=="sayak@sen.com" and password=="abc"):
			session['username'] = username
			print("Authenticated ")
			return redirect(url_for('home'))

	return render_template('login.html')


if __name__ == "__main__":
	app.run(debug=True)
