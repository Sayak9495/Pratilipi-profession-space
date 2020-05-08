from flask import Flask, render_template, g, request, session, redirect, url_for,abort
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug import secure_filename
from passlib.hash import sha256_crypt
from datetime import datetime,timedelta
import time, threading

app = Flask(__name__)
app.secret_key = 'qweqweqsfdqwfsdsghjyujlmbnvou'
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img/profile/'
configure_uploads(app, photos)
ENV = 'prod'
if ENV == 'dev':
	app.debug = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sayaksen:sayaksen@localhost/pratilipi'
else:
	app.debug = False
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cxfwjhdlyghphy:35f35daf343c82c5d8cc51e1976924f9b8488a206444846bf0672e2860dd5875@ec2-18-233-137-77.compute-1.amazonaws.com:5432/dcqnq6tpmk9dk6'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- DB MODELS ----------------------
class Auth(db.Model):
	__tablename__ = 'user_auth'
	email = db.Column(db.String(), primary_key=True)
	password = db.Column(db.String())

	def __init__(self, email, password):
		self.email = email
		self.password = password

class Company(db.Model):
	__tablename__ = 'company_details'
	name = db.Column(db.String(), primary_key=True)
	address = db.Column(db.String())
	total_views = db.Column(db.Integer)
	logo_path = db.Column(db.String())

	def __init__(self, name, address, total_views, logo_path):
		self.name = name
		self.address = address
		self.total_views = total_views
		self.logo_path = logo_path

class Users(db.Model):
	__tablename__ = 'user_details'
	email = db.Column(db.String(), db.ForeignKey('user_auth.email'), nullable=False, primary_key=True)
	name = db.Column(db.String())
	job_role = db.Column(db.String())
	company_name = db.Column(db.String(), db.ForeignKey('company_details.name'))
	profile_img_path = db.Column(db.String())

	def __init__(self, email, name, job_role, company_name, profile_img_path):
		self.email = email
		self.name = name
		self.job_role = job_role
		self.company_name = company_name
		self.profile_img_path = profile_img_path

class Pratilipi(db.Model):
	__tablename__ = 'pratilipi'
	email = db.Column(db.String(), db.ForeignKey('user_auth.email'), nullable=False, primary_key=True)
	date_time = db.Column(db.DateTime, nullable = False)

	def __init__(self, email):
		self.email = email
		self.date_time = datetime.now()

class Tesla(db.Model):
	__tablename__ = 'tesla'
	email = db.Column(db.String(), db.ForeignKey('user_auth.email'), nullable=False, primary_key=True)
	date_time = db.Column(db.DateTime, nullable = False)

	def __init__(self, email):
		self.email = email
		self.date_time = datetime.now()

class Spacex(db.Model):
	__tablename__ = 'spacex'
	email = db.Column(db.String(), db.ForeignKey('user_auth.email'), nullable=False, primary_key=True)
	date_time = db.Column(db.DateTime, nullable = False)

	def __init__(self, email):
		self.email = email
		self.date_time = datetime.now()

company_list = {"Pratilipi": Pratilipi, "Tesla": Tesla, "Spacex": Spacex}


# ---------------- APP ROUTES ----------------------
@app.before_request
def before_request():
	#get all infos from db here
	g.email = None
	if 'email' in session:
		g.email = session['email']

@app.route("/")
def index():
	return redirect(url_for('login'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	if (request.method == 'POST'):
		email = request.form['email']
		name = request.form['name']
		job_role = request.form['job_role']
		company_name = request.form['company_name']
		password = request.form['password']
		file_name = request.files['photo']
		if(email=='' or name=='' or job_role=='' or company_name=='' or file_name.filename==''):
			return render_template('signup.html', message="Empty string not accepted. Please try again.")
		if ((db.session.query(Users).filter(Users.email == email)).count() == 0):
			if ((db.session.query(Company).filter(Company.name == company_name)).count()):
				profile_img_path = email+".png"
				filename = photos.save(file_name, name=profile_img_path)
				
				password = sha256_crypt.encrypt(password)
				auth_data = Auth(email, password)
				db.session.add(auth_data)
				db.session.commit()

				profile_data = Users(email, name, job_role, company_name, profile_img_path)
				db.session.add(profile_data)
				db.session.commit()
				return render_template('login.html', message="Regestration Successfull. Please Login...")
			else:
				return 	render_template('signup.html', message="Company Name not registered. Please try with Pratilipi or Spacex or Tesla")
		else:
			return render_template('signup.html', message="Email Already exists. Try Logging in.")
	return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	if g.email:
		return redirect(url_for('home'))
	if (request.method == 'POST'):
		session.pop('email', None)
		email = request.form['email']
		password = request.form['password']

		if ((db.session.query(Auth).filter(Auth.email == email)).count()):
			pwd = db.session.query(Auth).filter(Auth.email == email)[0].password
			if (sha256_crypt.verify(password, pwd)):
				session['email'] = email
				return redirect(url_for('home'))
			else:
				return render_template('login.html', message="Wrong password")
		else:
			return render_template('login.html', message="email not registered")

	return render_template('login.html')

@app.route("/home")
def home():
	if not g.email:
		return redirect(url_for('signup'))
	data = db.session.query(Users).filter(Users.email == g.email)[0]
	data.profile_img_path = app.config['UPLOADED_PHOTOS_DEST']+data.profile_img_path
	return render_template('home.html', data=data)

@app.route("/company/<name>")
def company(name):
	global company_list
	if not g.email:
		return redirect(url_for('login'))
	data = db.session.query(Company).filter(Company.name == name)
	if (data.count()):
		data=data.first()
		data.total_views +=1
		db.session.commit()
		data.live_unique_view = len(db.session.query(company_list.get(name)).all())
		return render_template('company.html', data=data)
	return redirect(url_for('home'))

@app.route("/company_search")
def company_search():
	if not g.email:
		return redirect(url_for('home'))
	if (request.method == 'GET'):
		company_name = request.args.get('company_name')
		data = db.session.query(Company).filter(Company.name.like(company_name + "%")).all()
		return render_template('company_search.html', data=data)
	return redirect(url_for('home'))

@app.route("/logout")
def logout():
	session.pop('email', None)
	return render_template('login.html')

@app.route("/active_user")
def active_user():
	global company_list
	company_name = request.args.get('company_name')
	if (company_list.get(company_name) == None):
		abort(400)
	data = db.session.query(company_list.get(company_name)).filter(company_list.get(company_name).email == g.email).all()
	if (len(data)):
		data=data[0]
		data.date_time = datetime.now()
		db.session.commit()
	else:
		row = company_list.get(company_name)(g.email)
		db.session.add(row)
		db.session.commit()
	return ""

def delete_data():
	global company_list
	expiration_time = 10
	limit = datetime.now() - timedelta(seconds=expiration_time)
	for company_name in company_list:
		db.session.query(company_list.get(company_name)).filter(company_list.get(company_name).date_time < limit).delete()
		db.session.commit()
	threading.Timer(expiration_time, delete_data).start()

# Insert sample company data for testing
def add_company():
	pratilipi_data = Company("Pratilipi", "Hosur Main Road, Bangalore, Karnataka 560029", 0, "https://media.glassdoor.com/sqll/1454725/pratilipi-squarelogo-1481798656702.png")
	tesla_data = Company("Tesla", "Palo Alto, California, United States", 0, "https://www.logocentral.info/wp-content/uploads/2020/04/Tesla-Logo-640X590.jpg")
	spacex_data = Company("Spacex", "Hawthorne, California, United States", 0, "https://cdn.dribbble.com/users/610788/screenshots/5157282/spacex.png")
	db.session.add(pratilipi_data)
	db.session.add(tesla_data)
	db.session.add(spacex_data)
	db.session.commit()

db.create_all()
add_company()
delete_data()
db.session.commit()

if __name__ == "__main__":
	app.run(debug=True)
