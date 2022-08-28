import json
from application import app,db,api
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,Response,session
from application.models import User,Course,Enrollment
from application.forms  import LoginForm, RegistrationForm
try: 
    from flask_restplus import Api, Resource
except ImportError:
    import werkzeug, flask.scaffold
    werkzeug.cached_property = werkzeug.utils.cached_property
    flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
    from flask_restplus import Api, Resource


##############################################################################
# @api.route('/api','/api/')
# class GetAndPost(Resource):
#     #get all users
#     def get(self):
#         return jsonify(User.objects.all())

#     #post a new user
#     def post(self):
#         data=api.payload
#         user=User(user_id=data['user_id'],  first_name=data['first_name'], last_name=data['last_name'],email=data['email'],)
#         user.set_password(data['password'])
#         user.save()
#         return jsonify(User.objects(user_id=data['user_id']))


# @api.route('/api/<idx>','/api/<idx>/')
# class GetUpdateDelete(Resource):
#     #get user by id
#     def get(self,idx):
#         return jsonify(User.objects(user_id=idx))

#     #update user by id
#     def put(self,idx):
#         data=api.payload
#         User.objects(user_id=idx).update(**data)
#         # user.first_name=data['first_name']
#         # user.last_name=data['last_name']
#         # user.email=data['email']
#         # user.set_password(data['password'])
#         # user.save()
#         return jsonify(User.objects(user_id=idx))

#     #delete user by id
#     def delete(self,idx):
#         User.objects(user_id=idx).delete()
#         return jsonify(User.objects(user_id=idx))
    




##############################################################################





@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html',index=True)

@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('username'):
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        user=User.objects(email=email).first()

        if user:
            if user and user.get_password(password):
                flash(f'Hi, {user.first_name}, you have been logged in!','success')
                session['user_id']=user.user_id
                session['username']=user.first_name
                return redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check username and password.','danger')
    return render_template('login.html',login=True,form=form,title='Login')

@app.route('/courses/')
@app.route('/courses/<term>')
def courses(term=None):
    if term is None:
        term='Fall 2022'
    courses=Course.objects.order_by('+courseID')

    return render_template('courses.html',courseData=courses,term=term,courses=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))




@app.route('/register',methods=['GET','POST'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user_id=User.objects.count()+1
        first_name=form.first_name.data
        last_name=form.last_name.data
        email=form.email.data
        password=form.password.data

        user=User(user_id=user_id,first_name=first_name,last_name=last_name,email=email)
        user.set_password(password)
        user.save()
        flash(f'Account created for {first_name} {last_name}!','success')
        return redirect(url_for('login'))
    return render_template('register.html',register=True,form=form,title='Register')


@app.route('/enrollment', methods=['POST','GET'])
def enrollment():
    if not session.get('username'):
        return redirect(url_for('login'))
    courseID=request.form.get('courseID')
    title=request.form.get('courseTitle')
    user_id=session.get('user_id')
    if courseID:
        if Enrollment.objects(user_id=user_id,courseID=courseID):
            flash(f'You are already enrolled in {courseID} {title}.','warning')
            return redirect(url_for('courses'))
        else:
            Enrollment(user_id=user_id,courseID=courseID).save()
            flash(f'You have been enrolled in {courseID} {title}.','success')

    classes = list( User.objects.aggregate(*[
            {
                '$lookup': {
                    'from': 'enrollment', 
                    'localField': 'user_id', 
                    'foreignField': 'user_id', 
                    'as': 'r1'
                }
            }, {
                '$unwind': {
                    'path': '$r1', 
                    'includeArrayIndex': 'r1_id', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'course', 
                    'localField': 'r1.courseID', 
                    'foreignField': 'courseID', 
                    'as': 'r2'
                }
            }, {
                '$unwind': {
                    'path': '$r2', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': user_id
                }
            }, {
                '$sort': {
                    'courseID': 1
                }
            }
        ]))
    
    return render_template('enrollment.html',classes=classes,enrollment=True,title='Enrollment')


# @app.route('/api/')
# @app.route('/api/<idx>')
# def api(idx=None):
#     if idx==None:
#         jdata=courseData
#     else:
#         jdata=courseData[int(idx)]
#     return Response(json.dumps(jdata), mimetype='application/json')




@app.route('/user')
def user():
    # User(user_id=1,first_name='John',last_name='Doe',email="test@uta.com",password="password").save()
    # User(user_id=2,first_name='Mary',last_name='Wu',email="testing@uta.com",password="password").save()
    users=User.objects.all()
    return render_template('user.html',users=users)