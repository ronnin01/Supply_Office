from flask import Blueprint, render_template, request, redirect, url_for, flash, session
#from .models import Itemsetup, Usertable, Category, Brand, Location, Department
#from . import db, app, photos
#from . import db
from .__init__ import connection
# from flask_mysqldb import MySQL
# import MySQLdb.cursors
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os.path
import random

auth = Blueprint('auth', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        conn = connection()
        cur = conn.cursor()
        cur.execute("Select UT_Email, UT_Password, UT_UserType, UT_Pic From usertable where UT_email = '" + email + "'")
        user = cur.fetchone()
        #user = Usertable.query.filter_by(UT_Email=email).first()
        cur.close()
        if(user):
            #if(user.UT_Password == password):
            if check_password_hash(user.UT_Password, password):
                session['email'] = user.UT_Email
                if user.UT_UserType == "Student":

                    session['user_image'] = user.UT_Pic

                    return redirect(url_for('auth.student_index_page'))
                else: 
                    return redirect(url_for('auth.admin_item_all'))
            else:
                flash("Incorrect Password", category='error')
        else:
            flash('Email Add does not exist', category='error')

    return render_template('signin.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@auth.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('auth.signin'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":

        ut_idno = request.form.get('ut_idno')
        ut_pic = request.files.get('ut_pic')
        ut_firstname = request.form.get('ut_firstname')
        ut_lastname = request.form.get('ut_lastname')
        ut_mi = request.form.get('ut_mi')
        ut_designation = request.form.get('ut_designation')
        ut_department = request.form.get('ut_department')
        ut_email = request.form.get('ut_email')
        ut_contact = request.form.get('ut_contact')
        ut_username = request.form.get('ut_username')
        ut_password = request.form.get('ut_password')
        ut_confirm_password = request.form.get('ut_confirm_password')

        if len(ut_password) < 6:
            flash('Password must be 6 above length', category='error')
        elif ut_password != ut_confirm_password:
            flash('Password is not match', category='error')
        elif ut_pic and allowed_file(ut_pic.filename):
        #else:
            #cur = db.connection.cursor()
            conn = connection()
            cur = conn.cursor()
            cur.execute("Select UT_Email from usertable where UT_email = '" + ut_email + "'")
            data = cur.fetchone()
            cur.close()
            if data:
                flash('Email already exist.', category='error')
            else:

                filename = secure_filename(ut_pic.filename)
                ut_pic.save(os.path.join('D:/Private/CIT Masteral files/Capstone 1 and 2 References/Capstone 2 files/requisition/website/static/uploads', filename))
            #ut_pic.save(os.path.join('C:/Users/Aaron Fulgar/Desktop/requisition/website/static/uploads', filename))
                
                #new_user = Usertable(
                #UT_IDNo = ut_idno,
                #UT_LastName = ut_lastname,
                #UT_FirstName = ut_firstname,
                #UT_MI = ut_mi,
                #UT_Contact = ut_contact,
                #UT_Email = ut_email,
                #UT_Pic = filename,
                #UT_Username = ut_username,
                #UT_Password = generate_password_hash(ut_password, method='sha256'),
                #UT_UserType = "Student",
                #UT_Designation = ut_designation,
                #UT_Department = ut_department
                #)
                #db.session.add(new_user)
                #db.session.commit()
                #cur =db.connection.cursor()
                conn = connection()
                cur = conn.cursor()
                cur.execute("INSERT INTO UserTable (UT_IDno, UT_LastName, UT_FirstName, UT_MI, UT_Contact, UT_Email,UT_Username, UT_Designation, UT_Password, UT_Pic) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",ut_idno, ut_lastname,ut_firstname, 
                ut_mi, ut_contact, ut_email,ut_username, ut_designation, generate_password_hash(ut_password, method='sha256'),filename)
                #db.connection.commit()
                conn.commit()
                conn.close()
                flash("You have been registered.")

                return redirect(url_for('auth.signin'))
        else:
            flash("Image must be png or jpg.", category='error')

    return render_template('signup.html')

@auth.route('/', methods=['GET', 'POST'])
def student_index_page():
    if 'user_image' not in session:
        return redirect(url_for('auth.signin'))
    else:
        return render_template('student_index_page.html')

@auth.route('/itemadd')
def itemadd():
    session['item'] = 'add'
    return redirect(url_for('auth.additem'))

# MAU NI NGA ROUTE FOR ADD SIR
@auth.route('/categoryadd', methods=['POST'])
def categoryadd():
    if request.method == "POST":
        conn = connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO Category(Cat_Name) VALUES(?)", request.form.get('category'))

        conn.commit()
        conn.close()

        flash("New Category Added to database", category="success")
        return redirect(url_for('auth.admin_item_entry'))



@auth.route('/admin/item/add', methods=['GET', 'POST'])
def admin_item_entry():
    if 'email' not in session:
        flash('Please login first', category='error')
        return redirect(url_for('auth.signin'))
    conn = connection()
    cur = conn.cursor()
    #if session['item'] == 'add':
        #brands = Brand.query.all()
        #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
        #cur = db.connection.cursor()
        
    cur.execute("Select * from Brand order by Br_BrandName")
    brand = cur.fetchall()
        
        #categories = Category.query.all()
        #cur = db.connection.cursor()
    cur.execute("Select * from Category order by Cat_Name")
    category = cur.fetchall()

        #user = Usertable.query.all()
        #cur = db.connection.cursor()
    cur.execute("Select Distinct UT_LastName, UT_FirstName, UT_UserID from UserTable where UT_UserType <> 'Student' order by UT_LastName")
    user = cur.fetchall()

        #location = Location.query.all()
        #cur = db.connection.cursor()
    cur.execute("Select * from Location order by Loc_Name")
    location = cur.fetchall()

        #department = Department.query.all()
        #cur = db.connection.cursor()
    cur.execute("Select Dept_No, Dept_Name from Department order by Dept_Name")
    department = cur.fetchall()

    if request.method == 'POST':
        IS_ItemName = request.form.get('txtItemName')
        IS_SerialNo = request.form.get('txtSerial')
        IS_ItemDesc = request.form.get('txtItemDesc')
        IS_CategoryNo = request.form.get('txtCategory')
        IS_Brand = request.form.get('txtBrand')
        IS_Model = request.form.get('txtModel')
        IS_Location = request.form.get('txtLocation')
        IS_Department = request.form.get('txtDepartment')
        IS_Owner = request.form.get('txtOwner')
        IS_BegStock = request.form.get('txtStocks')
        IS_Unit = request.form.get('txtUnit')
        IS_Pic = request.files.get('imgItem')
        #IS_UserNo = request.form.get('txtUserNo')
        if IS_Pic and allowed_file(IS_Pic.filename):
        #else:
            filename = secure_filename(IS_Pic.filename)

            IS_Pic.save(os.path.join('D:/Private/CIT Masteral files/Capstone 1 and 2 References/Capstone 2 files/requisition/website/static/uploads', filename))
            #photos.save(request.files.get('imgItem'))

            # new_item = Itemsetup(
            #     IS_ItemName = IS_ItemName,
            #     IS_SerialNo = IS_SerialNo,
            #     IS_ItemDesc = IS_ItemDesc,
            #     IS_CategoryNo = IS_CategoryNo,
            #     IS_Brand = IS_Brand,
            #     IS_Model = IS_Model,
            #     IS_Location = IS_Location,
            #     IS_Department = IS_Department,
            #     IS_Owner = IS_Owner,
            #     IS_BegStock = IS_BegStock,
            #     IS_Unit = IS_Unit,
            #     IS_Pic = filename)
            # db.session.add(new_item)
            # db.session.commit()
                #cur =db.connection.cursor()
            conn = connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO ItemSetup (IS_ItemName, IS_SerialNo, IS_ItemDesc, IS_CategoryNo, IS_Brand, IS_Model,IS_Location, IS_Department, IS_Owner, IS_BegStock, IS_Unit,IS_Pic) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(IS_ItemName, IS_SerialNo,IS_ItemDesc, 
            IS_CategoryNo, IS_Brand, IS_Model, IS_Location, IS_Department, IS_Owner, IS_BegStock,IS_Unit,filename))
            conn.commit()
            conn.close()
                #db.connection.commit()
            flash("New Item Added to database", category="success")
            return redirect(url_for('auth.admin_item_all'))
        else:
            flash("Image must be png or jpg.", category='error')
    return render_template('additem.html', brands = brand, categories = category, users = user, locations=location, departments=department)
    

@auth.route('/admin/items/all', methods=['GET', 'POST'])
def admin_item_all():
    if 'email' not in session:
        flash('Please login first', category='error')
        return redirect(url_for('auth.signin'))
    conn = connection()
    cur = conn.cursor()
    #item = Itemsetup.query.all()
    #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("Select * from ItemSetup left join Brand on ItemSetup.IS_Brand = Brand.Br_BrandId \
    left join Category on ItemSetup.IS_CategoryNo = Category.Cat_ID \
    left join Location on ItemSetup.IS_Location = Location.Loc_No \
    left join Department on ItemSetup.IS_Department = Department.Dept_No \
    left join Usertable on ItemSetup.IS_Owner = Usertable.UT_UserID \
    order by IS_DateAdded desc")
    item = cur.fetchall()
    cur.close()

        # return redirect(url_for('auth.signin'))
        #return render_template('index.html', data=0)
    return render_template('index.html', items=item)
    

@auth.route('/admin/item/borrow', methods=['GET', 'POST'])
def admin_item_borrow():
    if 'email' not in session:
        flash('Please login first', category='error')
        return redirect(url_for('auth.signin'))
    conn = connection()
    cur = conn.cursor()
    
    #item = Itemsetup.query.all()
    #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("Select * from ItemSetup left join Brand on ItemSetup.IS_Brand = Brand.Br_BrandId \
    left join Category on ItemSetup.IS_CategoryNo = Category.Cat_ID \
    left join Location on ItemSetup.IS_Location = Location.Loc_No \
    left join Department on ItemSetup.IS_Department = Department.Dept_No \
    left join Usertable on ItemSetup.IS_Owner = Usertable.UT_UserID \
    where BR_Brandname = 'Canon' order by IS_DateAdded desc")
    item = cur.fetchall()
    cur.close()

        # return redirect(url_for('auth.signin'))
        #return render_template('index.html', data=0)
    return render_template('index.html', items=item)