"""
from . import db
from sqlalchemy.sql import func

class Itemsetup(db.Model):
    IS_ItemNo = db.Column(db.Integer, primary_key=True)
    IS_SerialNo = db.Column(db.Integer)
    IS_ItemName = db.Column(db.String(100))
    IS_ItemDesc = db.Column(db.String(1000))
    IS_CategoryNo = db.Column(db.Integer)
    IS_Brand = db.Column(db.String(50))
    IS_Model = db.Column(db.String(50))
    IS_Location = db.Column(db.Integer)
    IS_Department = db.Column(db.Integer)
    IS_Owner = db.Column(db.Integer)
    IS_Pic = db.Column(db.String(100))
    IS_DateAdded = db.Column(db.DateTime(timezone=True), default=func.now())
    IS_BegStock = db.Column(db.Integer)
    IS_Unit = db.Column(db.String(20))
    IS_UserNo = db.Column(db.Integer)

class Usertable(db.Model):
    UT_UserID = db.Column(db.Integer, primary_key=True)
    UT_IDNo = db.Column(db.Integer)
    UT_FirstName = db.Column(db.String(100))
    UT_LastName = db.Column(db.String(100))
    UT_MI = db.Column(db.String(1))
    UT_Contact = db.Column(db.Integer)
    UT_Email = db.Column(db.String(50))
    UT_Pic = db.Column(db.String(100))
    UT_Username = db.Column(db.String(50))
    UT_Password = db.Column(db.String(50))
    UT_UserType = db.Column(db.String(20))
    UT_Designation = db.Column(db.Integer)
    UT_Department = db.Column(db.Integer)

class Stocks(db.Model):
    St_StockID = db.Column(db.Integer, primary_key=True)
    St_ItemNo = db.Column(db.Integer)
    St_Mode = db.Column(db.String(20))
    St_Date = db.Column(db.DateTime(timezone=True), default=func.now())

class Category(db.Model):
    Cat_ID = db.Column(db.Integer, primary_key=True)
    Cat_Name = db.Column(db.String(50))
    Cat_Desc = db.Column(db.String(200))
class Brand(db.Model):
    Br_BrandID = db.Column(db.Integer, primary_key=True)
    Br_BrandName = db.Column(db.String(50))
class Location(db.Model):
    Loc_ID = db.Column(db.Integer, primary_key=True)
    Loc_Name = db.Column(db.String(200))

class Department(db.Model):
    Dept_No = db.Column(db.Integer, primary_key=True)
    Dept_Name = db.Column(db.String(50))
    Dept_Desc = db.Column(db.String(200))
"""