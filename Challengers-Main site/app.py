"""This is a project made and implemented using Flask Framework with backend as SQLITE3 and front end designing in HTML5 and CSS3.
The purpose of the project was to develop a platform where high level programming competitions can be thrown with the well defined
deadline. We built this project and tested it by successfully organizing a National level programming Hackthon.
The project was developed within 10 days of time interval(9 August 2017- 19 August 2017).
This project is being developed by Ranajoy, BCA 3rd Semester, IITM, IP University, New Delhi- ranajoydutta7@gmail.com.
and Anant Kaushik (Front End Designer), BCA 3rd Semester, IITM, IP University, New Delhi- anant.kaushik2@gmail.com"""

from flask import Flask, render_template, request, redirect, url_for, flash, g, session
import sqlite3 as sql,os,pytz,random
from datetime import datetime
tz=pytz.timezone('Asia/Kolkata')

app = Flask(__name__,static_url_path='')
app.config["CACHE_TYPE"] = "null"
app.secret_key = os.urandom(24)

def slic(string):
     ta=str(string)
     sliced = ta[3:-4]
     return sliced

@app.route('/')
def index():                                 #Homepage
   return render_template("index.html")

@app.route('/login')
def login():
    if g.user:                               #If already logged in
        return redirect(url_for('maindash'))
    else:
        return render_template("login.html")

@app.route('/maindash')
def maindash():
    if g.user:                               #If already logged in
       return render_template('maindash.html',user=session['name'])
    return redirect(url_for('login'))

@app.route('/logout')                        #route to logout from the session
def logout():
  session.pop('user', None)
  return redirect(url_for('index'))

@app.route('/registration', methods=['GET','POST'])    #registration module
def addrec():
    localtime=datetime.now(tz);
    if (str(localtime) >'2017-09-03 00:00:00.000000+05:30' and str(localtime)<('2017-09-06 23:99:99.999999+05:30')):         #setting opening and closing time of registration
         if g.user:
             return redirect(url_for('maindash'))
         else:
             if request.method == 'POST':
                 lis={0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty'}
                 numb1=request.form['numb1']                #Captcha
                 numb=request.form['numb2']
                 check2=request.form['check']
                 for name, age in lis.items():
                     if age == numb:
                         numb2=name
                 check1=int(numb1)+int(numb2)
                 if str(check1)!=str(check2):
                     msg="Incorrect Captcha!"
                     num1=random.randint(0,500)
                     lis={0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty'}
                     num2=random.choice(lis)
                     return render_template('registration.html',msg=msg,num1=num1,num2=num2)
                 #if user passes all checks (reconfirm password, captcha)
                 if request.form['password'] == request.form['repassword']:          #Reconfirm Password Field
                     con=sql.connect('database_ch.db')                               
                     cur=con.cursor()
                     email = request.form['email']
                     email = email.lower()  
                     flag=0
                     cur.execute("select flag from users where email = ?",(email,))
                     a = cur.fetchone();
                     ta=str(a)
                     output=ta[2:-3]
                     cur.close()
                     con.close()
                     if (output == str(1)):
                          msg = "E-mail already registered"
                          num1=random.randint(0,500)
                          lis={0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty'}
                          num2=random.choice(lis)
                          return render_template('registration.html',msg=msg,num1=num1,num2=num2)
                     else:
                          name = request.form['name']
                          Roll_Number = request.form['Roll_Number']
                          college = request.form['college']
                          university = request.form['university']
                          password = request.form['password']
                          phone = request.form['phone']
                          email = request.form['email']
                          email = email.lower()
                          semester = request.form['semester']
                          flag=1
                          with sql.connect("database_ch.db") as con:
                              cur = con.cursor()
                              user_id=name[0:2]+'.'+email+'.'+Roll_Number[0:2]
                              cur.execute("INSERT INTO users (flag,name,roll_number,college,university,password,user_id,phone,email,semester)VALUES (?,?,?,?,?,?,?,?,?,?)",(flag,name,Roll_Number,college,university,password,user_id,phone,email,semester) )
                              con.commit()
                              msg = "Congrats! You have successfully registered! Please Login"
                              return render_template("login.html",error = msg)
                              cur.close()
                              con.close()
                 else:
                     msg = "repassword didnt Match"
                     num1=random.randint(0,500)
                     lis={0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty'}
                     num2=random.choice(lis)
                     return render_template('registration.html',msg=msg,num1=num1,num2=num2)
             else:
                 num1=random.randint(0,500)
                 lis={0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty'}
                 num2=random.choice(lis)
                 return render_template('registration.html',num1=num1,num2=num2)

    #This will execute if the registration timings have been closed
    return "<h1 align='center'>Registrations have been closed !!! Thank You four your cooperation<br/><a href='/'>Go to Home Page </a></h1>"

# This is route for Sign-In
@app.route('/search', methods = ['POST'])
def search():
    if request.method == 'POST':
        con = sql.connect("database_ch.db")       #Opening Database
        username = request.form['username']       #getting values from Log in page(from user)
        password= request.form['password']
        cur = con.cursor()
        username = username.lower()               #changing all inputs to lower case
        cur.execute("select password from users where email = ?",(username,))   #retrieving password from database, we have used email as primary key in the table
        a = cur.fetchone();
        ta=str(a)
        output=ta[2:-3]
        cur.execute("select name from users where email = ?",(username,))
        b = cur.fetchone();
        tb=str(b)
        name=tb[2:-3]
        session.pop('user', None)
        cur.close()
        con.close()

        if request.form['password'] == output and output != '':            #matching the credentials 
            session['user'] = username
            session['name'] = name
            return redirect(url_for('maindash'))
        else:
            error='Invalid Credentials! Please Try Again'
            return render_template('login.html',error=error)
    return render_template('login.html')

@app.route('/rules')                    
def rules():
    return render_template('rules.html')

@app.route('/pra',methods=['GET','POST'])                        # routing for Hackathon (answer) page
def pra():
     if request.method == 'POST':
          level = request.form['level']
          return redirect(url_for('prac',q=level))

@app.route('/prac/<q>')                                          # Routing to open next question
def prac(q):
    q=int(q)
    if q<15:
         q += 1
    else:
         q = 1
    return redirect(url_for('practice',i=q))

@app.route('/practice')
def prac_route():
     return redirect(url_for('practice',i=1))

@app.route('/practice/<i>')                            #main route for Hackthon Page (Retrieving and showing questions)
def practice(i):
   if not g.user:
       return redirect(url_for('login'))
   else:
       if (int(i)<=15):
            con = sql.connect("hack_it_v3.db")
            cur = con.cursor()
            con2 = sql.connect('hack_it_v3.db')
            cur2 = con2.cursor()
            val =None
            cur2.execute("select answer from answer where level = ? and email = ?",(i,g.user,))
            val = slic(cur2.fetchall());
            val = str(val)
            if val !="":
                 color = 'red'
            else:
                 color = 'black'

            cur.execute("select tit from ques where level=?",(i,))
            title = slic(cur.fetchall());

            cur.execute("select about from ques where level=?",(i,))
            about = slic(cur.fetchall());

            if int(i)==11:
                cur.execute("select extra from ques where level=11")
                extra = slic(cur.fetchall());
            else:
                extra=None

            cur.close()
            con.close()

            con1 = sql.connect("hack_it_v3.db")
            con1.row_factory = sql.Row
            cur1 = con1.cursor()

            cur1.execute("select * from ques where level <= 8")
            rows1 = cur1.fetchall();

            cur1.execute("select * from ques where level > 8 and level <= 13 ")
            rows2 = cur1.fetchall();

            cur1.execute("select * from ques where level >= 14")
            rows3 = cur1.fetchall();
            cur1.close()
            con1.close()

            cur2.close()
            con2.close() 

            return render_template("answer1.html",extra=extra,i=i,level=i,color=color,rows1=rows1,rows3=rows3,rows2=rows2,about=about,title=title,val=val)
       elif (int(i)<=15):
           return
       else:
            return redirect(url_for("maindash"))
    
@app.route('/submit',methods=['GET','POST'])                #Route for submission of answers
def ans():
    if request.method == 'POST':
        ans= request.form['ans']
        level=request.form['level']
        con=sql.connect('hack_it_v3.db')
        cur=con.cursor()
        localtime = datetime.now(tz)
        cur.execute("select time from answer where level = ? and email=?",(level,g.user,))
        check = slic(cur.fetchall());
        ans=ans.replace('\r\n','&#13;&#10;')                #replacing all tabs and new lines with their ascii values 
        print (check)
        if (check==""):
             print ("inserted")
        else:
             print ("updated")
        con.commit()
        cur.close()
        con.close()
        return redirect(url_for('practice',i=level))


def al():
     con = sql.connect("database_ch.db")
     con.row_factory = sql.Row
     cur = con.cursor()
     cur.execute("select * from users")
     rows = cur.fetchall();
     cur.close()
     con.close()
     return rows


@app.route('/admin/list')
def list():
    if g.user == "ranajoydutta7@gmail.com" or g.user == "anantkaushik2628@gmail.com" or g.user == "suruchi.sinha90@gmail.com" :         #allowing access only to the admin (all admins)
        con1 = sql.connect("database_ch.db")                #opening database having user information
        cur1 = con1.cursor()
        cur1.execute("select count(*) from users")          #retreiving all Information regarding the users
        coun = cur1.fetchall();
        coun=str(coun)
        coun=coun[2:-3]
        cur1.close()
        con1.close()
        rows = al()
        return render_template("tables.html",rows = rows,count=coun)
    else:
        return "<h1 align='center'>Prohibitted</h1>"        #If unauthorized users try to access this page (any user other than admin)

@app.route('/delrec',methods=['GET','POST'])
def delrec():
    if request.method == 'POST' and g.user == "ranajoydutta7@gmail.com":        #Only This admin can make any change in data present in database
         con1 = sql.connect("database_ch.db")
         cur1 = con1.cursor()
         cur1.execute("select count(*) from users")
         coun = cur1.fetchall();
         coun=str(coun)
         coun=coun[2:-3]
         cur1.close()
         con1.close()

         try:
              con = sql.connect("database_ch.db")
              cur = con.cursor()
              rec = request.form['email']                   #make any change by providing sqlite3 Commands
              cur.execute(rec)
              a=cur.fetchall();
              con.commit()
              cur.close()
              con.close()
              rows=al()
         except:
              a = "Failed"
         finally:
              return render_template('tables.html',rows=rows,error=a,count=coun)
    elif g.user != "ranajoydutta7@gmail.com":
         return """<h1 align = center>Trespassing Prohibited<br/>You Dont have enough permisions</h1>"""

@app.route('/language',methods=['GET','POST'])
def language():
     if request.method == 'POST':
        con=sql.connect('database_ch.db')
        cur=con.cursor()
        language = request.form['language']
        cur.execute("UPDATE users SET language = ? WHERE email = ?",(language, g.user))
        con.commit()
        cur.close()
        con.close()
        return redirect(url_for('prac_route'))

@app.route('/ringless_mail', methods = ['GET','POST'])                     #this is a broadcasting module
def broad():
     if g.user=='ranajoydutta7@gmail.com' or g.user=='suruchi.sinha90@gmail.com':
         con=sql.connect("database_ch.db")
         cur=con.cursor()
         cur.execute("select message from broadcast where user = 'admin'")
         inp=slic(cur.fetchall())
         con.commit()
         if request.method == 'POST':
              asd=request.form['ins']
              con=sql.connect("database_ch.db")
              cur=con.cursor()
              cur.execute("select message from broadcast where user = 'admin'")
              inp=slic(cur.fetchall())
              con.commit()

              if not inp:
                  inp="<div><h3>"+asd+"</h3></div>"
                  cur.execute('insert into broadcast (message) values (?)',(inp,))
                  con.commit()
              else:
                  inp=inp+"<div><h3>>>> "+asd+"</h3></div>"
                  cur.execute("UPDATE broadcast SET message = ? WHERE user='admin'",(inp,))
                  con.commit()

              return render_template("b.html",inpu=inp,user=g.user)
         cur.close()
         con.close()
         return render_template("b.html",inpu=inp,user=g.user)
     else:
         con=sql.connect("database_ch.db")
         cur=con.cursor()
         cur.execute("select message from broadcast where user = 'admin'")
         inp=slic(cur.fetchall())
         con.commit()
         cur.close()
         con.close()
         return render_template("b.html",inpu=inp)


@app.errorhandler(404)                  
def page_not_found(e):
    return '''<head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body style="background:url(https://i.ytimg.com/vi/2rss9qfMubw/maxresdefault.jpg);background-size:100% 100%;    background-repeat: no-repeat;"><h1 align="center" style="font-family:algerian;margin-top:7%; "><a href="/" style="color:white;">Go to Home</a></h1></body>''', 404

@app.errorhandler(500)
def internal_server_error(e):
    return '''<head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body style="background:url(https://i.ytimg.com/vi/XUbOCVk-BW8/maxresdefault.jpg);background-size:100% 100%;    background-repeat: no-repeat;"><h1 align="center" style="font-family:algerian;margin-top:7%; "><a href="/" style="color:white;">Go to Home</a></h1></body>''', 500

@app.errorhandler(405)
def method_not_allowed(e):
    return '''<head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body style="background:url(https://i.ytimg.com/vi/q5rIxpE3fjA/maxresdefault.jpg);background-size:100% 100%;    background-repeat: no-repeat;"><h1 align="center" style="font-family:algerian;margin-top:7%; "><a href="/" style="color:white;">Go to Home</a></h1></body>''', 405

if __name__ == '__main__':
   app.run(debug=True)
