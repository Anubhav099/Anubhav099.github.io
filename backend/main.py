from flask import Flask, json,redirect,render_template,flash,request
from flask.globals import request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from flask_mail import Mail
import json

local_server=True                                       
app=Flask(__name__)                                     
app.secret_key="anubhav"                                

with open('config.json','r') as c:
    params=json.load(c)["info"]

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME= params['gmail-user'],
    MAIL_PASSWORD= params['gmail-password']
)
mail = Mail(app)

login_manager=LoginManager(app)
login_manager.login_view='login'

#                             'mysql://username:password@localhost/database_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/game_review'
db=SQLAlchemy(app)

@login_manager.user_loader
def load_user(arg):
    return PLAYER.query.get(str(arg)) or ADMIN.query.get(str(arg)) or REVIEWER.query.get(str(arg))

class ADMIN(UserMixin,db.Model):
    def get_id(self):
           return (self.Ad_mail)
    Ad_mail=db.Column(db.String(40),primary_key=True)
    pw=db.Column(db.String(1000))

class PLAYER(UserMixin,db.Model):
    def get_id(self):
           return (self.username)
    username=db.Column(db.String(40),primary_key=True)
    P_mail=db.Column(db.String(40),unique=True)
    pw=db.Column(db.String(1000))
    Gender=db.Column(db.String(1))
    Age=db.Column(db.Integer)
    Preferred_Platform=db.Column(db.String(40))

class GAME(db.Model):
    GName=db.Column(db.String(40),primary_key=True)
    publisher=db.Column(db.String(40))
    Rel_Date=db.Column(db.String(40))
    avail_plat=db.Column(db.String(100))

class REVIEWER(UserMixin,db.Model):
    def get_id(self):
           return (self.R_mail)
    R_mail=db.Column(db.String(40))
    RID=db.Column(db.Integer,primary_key=True)
    pw=db.Column(db.String(1000))
    RName=db.Column(db.String(40))
    Gender=db.Column(db.String(1))
    Age=db.Column(db.Integer)

class REVIEW(db.Model):
    Hours_Played=db.Column(db.Integer)
    Body=db.Column(db.String(800))
    RID=db.Column(db.Integer,primary_key=True)
    GName=db.Column(db.String(40),primary_key=True)

@app.route("/")                                         
def home():
    return render_template("index.html")                

@app.route("/playersignup",methods=['POST','GET'])
def playersignup():
    if request.method=='POST':
        username=request.form.get('i_username')
        P_mail=request.form.get('i_P_mail')
        pw=request.form.get('i_pw')
        Gender=request.form.get('i_Gender')
        Age=request.form.get('i_Age')
        Preferred_Platform=request.form.get('i_Preferred_Platform')
        encpw=generate_password_hash(pw)
        player = PLAYER.query.filter_by(username=username).first()
        playermail = PLAYER.query.filter_by(P_mail=P_mail).first()
        if player or playermail:
            flash("Username or email already taken","danger")
            return render_template("signupplayer.html")
        new_player=db.engine.execute(f"INSERT INTO `player` (`username`,`P_mail`,`pw`,`Gender`,`Age`,`Preferred_Platform`) VALUES ('{username}','{P_mail}','{encpw}','{Gender}','{Age}','{Preferred_Platform}')")
        flash("Signup Successful, you can login.","success")
        return render_template("loginplayer.html")

    return render_template("signupplayer.html")

@app.route("/playerlogin", methods=['POST', 'GET'])
def playerlogin():
    if request.method == 'POST':
        username = request.form.get('i_username')
        pw = request.form.get('i_pw')
        player = PLAYER.query.filter_by(username=username).first()

        if player and check_password_hash(player.pw, pw):
            login_user(player)
            return redirect(url_for('mainpage'))
        else:
            flash("Invalid Credentials!","danger")
            return render_template("loginplayer.html")

    return render_template("loginplayer.html")


@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    if request.method=="POST":
        Ad_mail = request.form.get('i_Ad_mail')
        pw = request.form.get('i_pw')
        admin = ADMIN.query.filter_by(Ad_mail=Ad_mail).first()

        if admin and check_password_hash(admin.pw, pw):
            login_user(admin)
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")

    return render_template("loginadmin.html")

@app.route('/reviewerlogin',methods=['POST','GET'])
def reviewerlogin():
    if request.method=="POST":
        R_mail = request.form.get('i_R_mail')
        pw = request.form.get('i_pw')
        reviewer = REVIEWER.query.filter_by(R_mail=R_mail).first()

        if reviewer and check_password_hash(reviewer.pw, pw):
            login_user(reviewer)
            return render_template("index.html")
        else:
            flash("Invalid Credentials","danger")
            return render_template("loginreviewer.html")

    return render_template("loginreviewer.html")


@app.route("/adsignup",methods=['POST','GET'])
def adsignup():
    if request.method=='POST':
        Ad_mail = request.form.get('i_Ad_mail')
        pw = request.form.get('i_pw')
        encpw=generate_password_hash(pw)
        adminmail = ADMIN.query.filter_by(Ad_mail=Ad_mail).first()
        if adminmail:
            flash("Email already exists","danger")
            return render_template("signupadmin.html")
        new_admin=db.engine.execute(f"INSERT INTO `admin` (`Ad_mail`,`pw`) VALUES ('{Ad_mail}','{encpw}')")
        flash("Signup Successful, you can login.","success")
        return render_template("loginadmin.html")

    return render_template("signupadmin.html")

@app.route('/addreviewer',methods=['POST','GET'])
@login_required
def addreviewer():
    query=db.engine.execute(f"SELECT * FROM `REVIEWER`")
    if request.method=='POST':
        R_mail=request.form.get('i_R_mail')
        pw=request.form.get('i_pw')
        RName=request.form.get('i_RName')
        Gender=request.form.get('i_Gender')
        Age=request.form.get('i_Age')
        encpw=generate_password_hash(pw)
        checkrev=REVIEWER.query.filter_by(R_mail=R_mail).first()
        if checkrev:
            flash("Reviewer Mail already exists","danger")
            return render_template("addreviewer.html",query=query)
        new_reviewer=db.engine.execute(f"INSERT INTO `reviewer` (`RID`, `R_mail`, `pw`, `RName`, `Gender`, `Age`) VALUES (NULL, '{R_mail}','{encpw}','{RName}','{Gender}','{Age}')")
        
        mail.send_message(
        'YOU ARE A GAME REVIEWER',            # Subject of the email
        sender=params['gmail-user'],           # Sender's email address
        recipients=[R_mail],                   # List of recipient email addresses
        body=f"Thanks for choosing to work with us\nYour Login Credentials Are:\n Email Address: {R_mail}\nPassword: {pw}\n\n Do not share your password\n\n\nThank You..."
        )

        flash("New Reviewer Added!","success")
        return redirect(url_for('addreviewer',query=query))
    return render_template("addreviewer.html",query=query)

@app.route('/logoutplayer')
@login_required
def logoutplayer():
    logout_user()
    flash("Logout SuccessFul","warning")
    return render_template("loginplayer.html")

@app.route('/logoutadmin')
@login_required
def logoutadmin():
    logout_user()
    flash("Logout SuccessFul","warning")
    return render_template("loginadmin.html")

@app.route('/logoutrev')
def logoutrev():
    logout_user()
    flash("Logout SuccessFul","warning")
    return render_template("loginreviewer.html")

@app.route('/addgame',methods=['POST','GET'])
@login_required
def addgame():
    query=db.engine.execute(f"SELECT * FROM `GAME`")
    if request.method=='POST':
        GName = request.form.get('i_GName')
        publisher = request.form.get('i_publisher')
        publisher = request.form.get('i_publisher')
        Rel_Date = request.form.get('i_Rel_Date')
        avail_plat = request.form.get('i_avail_plat')

        checkgame=GAME.query.filter_by(GName=GName).first()
        if checkgame:
            flash("Game already exists","danger")
            return render_template("addgame.html",query=query)
        new_game=db.engine.execute(f"INSERT INTO `game` (`GName`,`publisher`,`Rel_Date`,`avail_plat`) VALUES ('{GName}','{publisher}','{Rel_Date}','{avail_plat}')")
        flash("New Game Added!","success")
        return redirect(url_for('addgame',query=query))

    return render_template("addgame.html",query=query)



@app.route('/test')
def test():
    return render_template("bootstrap.html")


@app.route('/addreview',methods=['POST','GET'])
def addreview():
    query=db.engine.execute(f"SELECT * FROM `GAME`")
    rquery=db.engine.execute(f"SELECT * FROM `REVIEWER`")

    if request.method=='POST':
        GName=request.form.get('i_GName')
        Body=request.form.get('i_Body')
        Hours_Played=request.form.get('i_Hours_Played')
        RID=request.form.get('i_RID')
        checkgame=GAME.query.filter_by(GName=GName).first()
        checkRID=REVIEWER.query.filter_by(RID=RID).first()
        checkGName=REVIEW.query.filter_by(GName=GName,RID=RID).first()
        if checkgame and checkRID and not checkGName:
            new_review=db.engine.execute(f"INSERT INTO `review` (`Hours_Played`, `Body`, `RID`, `GName`) VALUES ('{Hours_Played}','{Body}','{RID}','{GName}')")
            flash("New Review published!","success")
            return redirect(url_for("addreview",query=query,rquery=rquery))
        else:
            flash("Review already exists or incorrect info","danger")
            return render_template("addreview.html",query=query,rquery=rquery)
        
    return render_template("addreview.html",query=query,rquery=rquery)

@app.route('/deletegame',methods=['POST','GET'])
@login_required
def deletegame():
    query=db.engine.execute(f"SELECT * FROM `GAME`")
    if request.method=='POST':
        GName=request.form.get('i_GName')
        checkgame=GAME.query.filter_by(GName=GName).first()
        if checkgame:
            del_game=db.engine.execute(f"DELETE FROM `game` WHERE `game`.`gname`='{GName}'")
            flash("Game Deleted!","success")
            return redirect(url_for('deletegame',query=query))
        else:
            flash("Match not found","danger")
            return render_template("deletegame.html",query=query)
        
    return render_template("deletegame.html",query=query)

@app.route('/updategame',methods=['POST','GET'])
def updategame():
    query=db.engine.execute(f"SELECT * FROM `GAME`")
    if request.method=='POST':
        GName=request.form.get('i_GName')
        publisher=request.form.get('i_publisher')
        Rel_Date=request.form.get('i_Rel_Date')
        avail_plat=request.form.get('i_avail_plat')
        checkgame=GAME.query.filter_by(GName=GName).first()
        if checkgame:
            update_game=db.engine.execute(f"UPDATE `game` SET `publisher`='{publisher}',`Rel_Date`='{Rel_Date}',`avail_plat`='{avail_plat}' WHERE `game`.`gname`='{GName}'")
            flash("Game Updated!","primary")
            return redirect(url_for('updategame',query=query))
        else:
            flash("Incorrect Game Name","danger")
            return render_template("updategame.html",query=query)
        
    return render_template("updategame.html",query=query)

@app.route('/New_Releases')
def New_Releases():
    query=db.engine.execute(f"SELECT * FROM `triggered` ORDER BY `triggered`.`Time` DESC")
    return render_template("New_Releases.html",query=query)

@app.route('/mainpage')
def mainpage():
    query=db.engine.execute(f"SELECT * FROM `GAME` NATURAL JOIN `REVIEW` INNER JOIN `REVIEWER` ON `REVIEW`.`RID`=`REVIEWER`.`RID` ORDER BY `GAME`.`GName` ASC")
    return render_template("mainpage.html",query=query)

@app.route('/aboutgame')
def aboutgame():
    thisgame=GAME.query.filter_by(GName=thisgame).first()

    return render_template("aboutgame.html")

app.run(debug=True)                                     #runs the application   