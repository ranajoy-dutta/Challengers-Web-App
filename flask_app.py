from flask import Flask, render_template, request, redirect, url_for, g, session
import sqlite3 as sql,os

app = Flask(__name__,static_url_path='')
app.secret_key = os.urandom(24)

def slic(string):
     ta=str(string)
     sliced = ta[3:-4]
     return sliced

def slic1(string):
     ta=str(string)
     sliced = ta[2:-3]
     return sliced

@app.route('/',methods=['GET','POST'])
def all():
     if g.user:
          i=1
          return redirect(url_for('check',i=i))
     else:
          if request.method=='POST':
               password=request.form['password']
               i=1
               session.pop('user', None)
               if password=='recheckall' or password=='secondcheck':
                    session['user'] = password
                    return redirect(url_for('check',i=i))
               else:
                    msg="Invalid Credentials !"
                    return render_template('all.html',msg=msg)
          return render_template("all.html")


@app.before_request
def before_request():
     g.user = None
     if 'user' in session:
          g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return 'Not logged in!'

@app.route('/logout')
def logout():
     session.pop('user', None)
     return redirect(url_for('all'))

@app.route('/check/<i>')
def check(i):
     if g.user:
          ques=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
          con=sql.connect("/home/anantkaushik/mysite/database_ch.db")
          cur=con.cursor()
          cur.execute('select level from answer where sno=?',(i,))
          level=cur.fetchall()
          level=str(level)
          level=level[2:-3]
          level=int(level)
          if level in ques:
               updated,checked1,checked2=2,2,2
               cur.execute('select updated,checked1,checked2 from answer where sno=?',(i,))
               flag=cur.fetchall()
               flag=str(flag)
               updated=flag[1:-2]
               print(flag)
               updated=int(str(flag)[2:-8])
               checked1=int(str(flag)[4:-5])
               checked2=int(str(flag)[8:-2])
               cur.execute('select input_test_case from answer where sno=?',(i,))
               input_case=slic1(cur.fetchall());

               cur.execute('select variation_test_case from answer where sno=?',(i,))
               var=slic1(cur.fetchall());

               cur.execute('select garbage_test_case from answer where sno=?',(i,))
               gar=slic1(cur.fetchall());

               cur.execute('select total1 from answer where sno=?',(i,))
               total1=slic1(cur.fetchall());

               cur.execute('select user_defined_function from answer where sno=?',(i,))
               user_defined=slic1(cur.fetchall());

               cur.execute('select indentation from answer where sno=?',(i,))
               indent=slic1(cur.fetchall());

               cur.execute('select total2 from answer where sno=?',(i,))
               total2=slic1(cur.fetchall());

               cur.execute('select extra_variable from answer where sno=?',(i,))
               extra_var=slic1(cur.fetchall());

               cur.execute('select Cummilative from answer where sno=?',(i,))
               cumm=slic1(cur.fetchall());

               cur.execute('select time_taken from answer where sno=?',(i,))
               time=slic1(cur.fetchall());

               cur.execute('select checked1 from answer where sno=?',(i,))
               checked1=slic1(cur.fetchall());

               cur.execute('select checked2 from answer where sno=?',(i,))
               checked2=slic1(cur.fetchall());

               cur.execute('select updated from answer where sno=?',(i,))
               updated=slic1(cur.fetchall());

               cur.execute('select language from users where email=(select email from answer where sno=?)',(i,))
               a=slic(cur.fetchall())

               cur.execute("select tit from ques where level =(select level from answer where sno=?)",(i,))
               b=slic(cur.fetchall())

               cur.execute("select about from ques where level =(select level from answer where sno=?)",(i,))
               c=slic(cur.fetchall())

               cur.execute("select count(email) from answer where checked2=1")
               d=str(cur.fetchall())
               d=int(d[2:-3])
               e=355-d
               val =None
               cur.execute("select answer from answer where sno=?",(i,))
               val = slic(cur.fetchall());
               val=val.replace('\r\n','&#13;&#10;')
               con.close()
               return render_template('answer1.html',quesn=level,language=a,ques=b,i=i,val=val,desc=c,d=d,e=e,input_case=input_case,var=var,gar=gar,total1=total1,user_defined=user_defined,indent=indent,total2=total2,extra_var=extra_var,cumm=cumm,time=time,checked1=checked1,checked2=checked2,updated=updated)
          else:
               con.close()
               return redirect(url_for('prac',q=i))
     else:
          return "<h1 align='center'>Plz Login!</h1>"


@app.route('/pra',methods=['GET','POST'])
def pra():
     if request.method=='POST':
          i=request.form['level']

          return redirect(url_for('prac',q=i))

@app.route('/prac/<q>')
def prac(q):
    q=int(q)
    q += 1
    return redirect(url_for('check',i=q))
"""
@app.route('/res',methods=['GET','POST'])
def res():
     if request.method == 'POST':
          con=sql.connect("/home/anantkaushik/mysite/database_ch.db")
          cur=con.cursor()
          input_test_case = int(request.form['input_test_case'])
          variation_test_case = int(request.form['variation_test_case'])
          garbage_test_case = int(request.form['garbage_test_case'])
          total1 = input_test_case + variation_test_case + garbage_test_case
          i = int(request.form['i'])
          user_defined_function = int(request.form['user_defined_function'])
          indentation = int(request.form['indentation'])
          total2 = indentation + user_defined_function
          time_taken = int(request.form['time_taken'])
          flag=1
          extra_variable = int(request.form['extra_variable'])
          cummilative = total1 + total2 + extra_variable
          cur.execute("update answer set input_test_case=?,variation_test_case=?,garbage_test_case=?,total1=?,user_defined_function=?,indentation=?,total2=?,extra_variable=?,Cummilative=? where sno=?",(input_test_case,variation_test_case,garbage_test_case,total1,user_defined_function,indentation,total2,extra_variable,cummilative,i))
          cur.execute("update answer set flag=1,time_taken=? where sno=?",(time_taken,i,))
          con.commit()
          cur.close()
          con.close()
          return redirect(url_for('prac',q=i))
     else:
          print('asdadada')
"""

@app.route('/update',methods=['GET','POST'])
def update():
     if request.method == 'POST':
          try:
               con=sql.connect("/home/anantkaushik/mysite/database_ch.db")
               cur=con.cursor()
               input_test_case = int(request.form['input_test_case'])
               variation_test_case = int(request.form['variation_test_case'])
               garbage_test_case = int(request.form['garbage_test_case'])
               total1 = input_test_case + variation_test_case + garbage_test_case
               i = int(request.form['i'])
               user_defined_function = int(request.form['user_defined_function'])
               indentation = int(request.form['indentation'])
               total2 = indentation + user_defined_function
               time_taken = int(request.form['time_taken'])
               flag=1
               extra_variable = int(request.form['extra_variable'])
               cummilative = total1 + total2 - extra_variable +time_taken
               if g.user=='secondcheck':
                    cur.execute("update answer set input_test_case=?,variation_test_case=?,garbage_test_case=?,total1=?,user_defined_function=?,indentation=?,total2=?,extra_variable=?,Cummilative=? where sno=?",(input_test_case,variation_test_case,garbage_test_case,total1,user_defined_function,indentation,total2,extra_variable,cummilative,i))
                    cur.execute("update answer set updated=1,checked1=1,checked2=1,time_taken=? where sno=?",(time_taken,i,))
               elif g.user=='recheckall':
                    cur.execute("update answer set input_test_case=?,variation_test_case=?,garbage_test_case=?,total1=?,user_defined_function=?,indentation=?,total2=?,extra_variable=?,Cummilative=? where sno=?",(input_test_case,variation_test_case,garbage_test_case,total1,user_defined_function,indentation,total2,extra_variable,cummilative,i))
                    cur.execute("update answer set updated=1,checked1=1,time_taken=? where sno=?",(time_taken,i,))
               else:
                    return "<h1 align='center'>Login plz!</h1>"
               con.commit()
               cur.close()
               con.close()
               return redirect(url_for('prac',q=i))
          except:
               con.rollback()
               return "<h1 align='center'>Transaction failed!</h1>"

@app.route('/checked',methods=['GET','POST'])
def checked():
     if request.method == 'POST':
          try:
               con=sql.connect("/home/anantkaushik/mysite/database_ch.db")
               cur=con.cursor()
               i = int(request.form['level'])
               if g.user=='secondcheck':
                    cur.execute("update answer set checked1=1,checked2=1 where sno=?",(i,))
               elif g.user=='recheckall':
                    cur.execute("update answer set checked1=1 where sno=?",(i,))
               else:
                    return "<h1 align='center'>Login plz!</h1>"
               con.commit()
               cur.close()
               con.close()
               return redirect(url_for('prac',q=i))
          except:
               con.rollback()
               return "<h1 align='center'>Transaction failed!</h1>"


@app.route('/table')
def table():
       con1 = sql.connect("/home/anantkaushik/mysite/database_ch.db")
       con1.row_factory = sql.Row
       cur1 = con1.cursor()
       cur1.execute("select sno,input_test_case,variation_test_case,garbage_test_case,total1,user_defined_function,indentation,total2,extra_variable,cummilative from answer where (flag=1) and (cummilative <> 0) order by sno;")
       rows = cur1.fetchall();
       cur1.close()
       con1.close()
       return render_template('tables.html',rows=rows)

@app.errorhandler(500)
def internal_server_error(e):
    return '''<head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head><body style="background:url(https://i.ytimg.com/vi/XUbOCVk-BW8/maxresdefault.jpg);background-size:100% 100%;    background-repeat: no-repeat;"><h1 align="center" style="font-family:algerian;margin-top:7%; "><a href="/" style="color:white;">Go to Home</a></h1></body>''', 500

if __name__ == '__main__':
   app.run(debug=True)

