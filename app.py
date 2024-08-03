from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eba0e8a172ea43274c416ae379e77b50'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crop_system'
mysql = MySQL(app)

if mysql.connection:
    print("Connection established successfully!")
else:
    print("Failed to establish a connection.")

@app.route("/")
def index():
    if 'user_id' in session and session['user_id']:
        return redirect(url_for('home'))
    else:
        return render_template('index.html', title="Login")

@app.route("/sign-up",methods=['GET','POST'])
def signup():
    error=''
    success=''
    if request.method == 'POST':
        email = request.form['email']
        name =request.form['name']
        password =request.form['password']

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        if not email or not name or not password:
            error = "All Fields Required"
            return render_template('index.html',errorMsg=error)
      
        else:
            cur = mysql.connection.cursor()

                # Check if the email already exists
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cur.fetchone()

            if existing_user:
                error="email already exist"
                return render_template('index.html',errorMsg=error)
            else:
                cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                            (name, email,hashed_password))
                mysql.connection.commit()
                cur.close()
                success="Registration Successful! Please Log In Now"
                return render_template('index.html', successMsg=success)
            

@app.route("/sign-in",methods=['GET','POST'])
def signin():
    
    error=''
    if request.method == 'POST':
        email = request.form['email']
        password =request.form['password']
       
        if not email or not password:
            error = "All Fields Required"
            return render_template('index.html',errorMsgSignIn=error)
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()

            if user and check_password_hash(user[3], password):
                session['user_id'] = user[0] 
                return redirect(url_for('home'))
            
            else:
            # Passwords do not match, authentication failed
                error="Invalid email or password"
                return render_template('index.html', errorMsgSignIn=error)
            
    return render_template('index.html')

@app.route('/logout')
def logout():
    # Clear the session and redirect to the login page
    session.pop('user_id',None)
    return redirect(url_for('index'))
    
           
@app.route("/home")
def home():
    if 'user_id' in session and session['user_id']:
        return render_template('home.html', title="Home")
    else:
        return redirect(url_for('index'))

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/feedback")
def feedback():
    if 'user_id' in session and session['user_id']:
        return render_template('feedback.html', title="Feedback")
    else:
        return redirect(url_for('index'))

@app.route("/feedbacksubmit", methods=['GET', 'POST'])
def feedbacksubmit():
    success=''
    if request.method == 'POST':
        name =request.form['name']
        email = request.form['email']
        message= request.form['message']
        question= request.form['question']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feedback (name, email, message,question) VALUES (%s, %s, %s,%s)",
                            (name, email,message,question))
        mysql.connection.commit()
        cur.close()
        successMsgfeedback="Thank You! Your feedback has been submitted."

        flash(successMsgfeedback)
        
        return redirect(url_for('feedback'))
    else:
        return redirect(url_for('feedback'))
    

@app.route("/contact")
def contact():
    return render_template('contact.html', title="Contact")


@app.route("/profile")
def profile():
    user_id = session['user_id']
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    return render_template('profile.html', title="profile", user_data=user_data)

    
@app.route("/admin-login")
def adminLogin():
    if 'role' in session and session['role']:
        return redirect(url_for('adminIndex'))
    else:
        return render_template('admin/admin-login.html', title="Admin Login")
    

@app.route("/admin-index")
def adminIndex():
    if 'role' in session and session['role']:
        return render_template('admin/admin-index.html', title="Admin Login")
    else:
        return redirect(url_for('index'))

@app.route("/admin-signin", methods=['POST'])
def adminSignIn():
    error=''
    if request.method == 'POST':
        username = request.form['username']
        password =request.form['password']
       
        if not username or not password:
            error = "All Fields Required"
            return render_template('admin/admin-login.html',errorMsgSignIn=error)
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM admin WHERE username = %s", (username,))
            admin = cur.fetchone()
            cur.close()

            if admin and check_password_hash(admin[4], password):
                session['role'] = admin[5] 
                return redirect(url_for('adminIndex'))
            
            else:
            # Passwords do not match, authentication failed
                error="Invalid email or password"
                flash(error)
                return redirect(url_for('adminLogin'))
            
    else:       
        return render_template('admin/admin-login.html')
    

# @app.route("/admin-signup",methods=['GET','POST'])
# def adminSignup():
    error=''
    success=''
    if request.method == 'POST':
        email = request.form['email']
        name =request.form['name']
        password =request.form['password']

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        if not email or not name or not password:
            error = "All Fields Required"
            return render_template('index.html',errorMsg=error)
      
        else:
            cur = mysql.connection.cursor()

                # Check if the email already exists
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cur.fetchone()

            if existing_user:
                error="email already exist"
                return render_template('index.html',errorMsg=error)
            else:
                cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                            (name, email,hashed_password))
                mysql.connection.commit()
                cur.close()
                success="Registration Successful! Please Log In Now"
                return render_template('index.html', successMsg=success)
            
@app.route("/category", methods=['get','post'])
def addCategory(): 
    msg = ''
    if request.method == 'POST':
        category_title = request.form.get('categoryTitle')
        category_types = request.form.get('categoryType')
        category_slug = request.form.get('categorySlug')
        status = request.form.get('status')
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO category (categoryTitle, categorySlug, categoryType, status) VALUES (%s, %s, %s, %s)",
                            (category_title, category_slug, category_types, status))
        
        mysql.connection.commit()
        cur.close()

        # Redirect to the view category page after adding a new category
        return render_template('admin/admin-category.html', msg="Category Added Successfully")
    else:
       return render_template('admin/admin-category.html', title="Category")
    
@app.route('/view_category')
def viewCategory():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM category")
    categories = cur.fetchall()
    cur.close()
    return render_template('admin/view-category.html', categories=categories)
    
@app.route('/add_dieases')
def addDieases():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM category")
    categories = cur.fetchall()
    cur.close()
    return render_template('admin/add-diseases.html',title="Add Diseases", categories=categories)

@app.route('/save_disease',  methods=['get','post'])
def saveDisease():
    msg = ''
    if request.method == 'POST':
        disease_title = request.form.get('diseaseTitle')
        disease_types = request.form.get('diseaseSlug')
        disease_slug = request.form.get('diseaseCategory')
        status = request.form.get('status')
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO diseases (diseaseTitle, diseaseSlug, diseaseCategory, diseaseStatus) VALUES (%s, %s, %s, %s)",
                            (disease_title, disease_types, disease_slug, status))
        
        mysql.connection.commit()
        cur.close()

        return render_template('admin/add-diseases.html', msg="Disease Added Successfully")
    else:
       return render_template('admin/add-diseases.html', title="Add Diseases")
    
@app.route('/view_diseases')
def viewDiseases():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM diseases")
    diseases = cur.fetchall()
    cur.close()
    return render_template('admin/view-diseases.html',diseases=diseases )
    
@app.route('/add_solution')
def addSolution():
    return render_template('admin/add-solution.html',title="Solution")

@app.route('/admin_logout')
def adminlogout():
    # Clear the session and redirect to the login page
    session.pop('user_id',None)
    return render_template('admin/admin-login.html', title="Admin Login")

# MODEL PREDICTION API
# model = tf.keras.models.load_model('models/3')

# class_names = ['Potato_EarlyBlight', 'Potato_Healthy', 'Potato_LateBlight', 'Sugarcane_Healthy', 'Sugarcane_Mosaic', 'Sugarcane_RedRot', 'Sugarcane_Rust', 'Sugarcane_Yellow']

# def read_file_as_image(data, target_size=(256, 256)) -> np.ndarray:
#     image = Image.open(BytesIO(data))
#     image = image.resize(target_size)
#     image = np.array(image)
#     return image

# @app.route('/api/prediction', methods=["POST"])
# def modelPrediction():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'})
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'})
#     if file:
#         image = read_file_as_image(file.read())
#         img_batch = np.expand_dims(image, 0)
        
#         predictions = model.predict(img_batch)

#         predicted_class = class_names[np.argmax(predictions[0])]
#         confidence = np.max(predictions[0])
#         confidence_rounded = int(round(float(confidence * 100)))
#         return {
#             'class': predicted_class,
#             'confidence': confidence_rounded
#         }
if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)