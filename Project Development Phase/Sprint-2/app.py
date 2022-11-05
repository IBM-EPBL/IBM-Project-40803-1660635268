from flask import Flask,render_template,redirect,url_for,request,make_response
import sqlite3 as sql
import jwt
import uuid
from datetime import datetime, timedelta

def verify(token):
    data = jwt.decode(token, "Hello", algorithms='HS256')
    return data["email"]

app=Flask(__name__,static_folder="static")

@app.route("/signin",methods=["POST","GET"])
def signin():
    if request.method=="GET":
        return render_template("signin.html")
    else:
        
        email=request.form["email"]
        password=request.form["password"]
        print(email,password)

        with sql.connect("donar.db") as connection:
            cursor=connection.cursor()
            cursor.execute("SELECT email,password FROM DONARS WHERE email=?",(email,))
            donar=cursor.fetchone()
        
            print(donar)
            print(donar[1])
            
            if donar==None:
                redirect("/signin")
            else:
                token = jwt.encode({"email": email, 'exp': datetime.utcnow(
                )+timedelta(minutes=30)}, "Hello", algorithm='HS256')
                print(token)

                response = make_response(
                    render_template("./home.html"))
                response.set_cookie('token', token)
                return response

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="GET":

        return render_template("signup.html")
    else:
        name=request.form["name"]
        email=request.form["email"]
        phone=request.form["phone"]
        password=request.form["password"]
        re_password=request.form["re-password"]
        key=uuid.uuid1().hex
        print(name,email,phone,password,re_password,key)

        if (password==re_password):
            with sql.connect("donar.db") as connection:
            
                cur=connection.cursor();
                cur.execute("INSERT INTO DONARS (id,name,email,phone,password) VALUES (?,?,?,?,?)",(key,name,email,phone,password))
                connection.commit()

                print("successfully added")
                return redirect("/home")

        else:
            return "Invalid response"

@app.route("/signout")
def logout():
    response = make_response(render_template("./signin.html"))
    response.set_cookie('token', '')
    return response

@app.route("/home")
def home():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        print(email)
        return render_template("./home.html")
    except:
        return redirect("./signin")

@app.route("/profile")
def profile():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        print(email)
        return render_template("./profile.html")
    except:
        return redirect("./signin")

@app.route("/plasma-request")
def plasma():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        return render_template("./plasma.html")
    except:
        return redirect("./signin")


@app.route("/donar-list")
def donar_list():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        return render_template("./donar-list.html")
    except:
        return redirect("./signin")

@app.route("/donar-registration",methods=["POST","GET"])
def donar_registration():
    if request.method=="GET":

        try:
            token = request.cookies.get('token')
            email = verify(token)
            print(email)
            return render_template("./donar.html")

        except:
            return redirect("/signin")

    else:
        try:
            token = request.cookies.get('token')
            email = verify(token)
            

            name=request.form["name"]
            phone=request.form["phone"]
            age=request.form["age"]
            blood=request.form["blood-group"]
            weight=request.form["weight"]
            parasitic=request.form["parasitic"]
            positive=request.form["positive"]
            negative=request.form["negative"]
            print(name,phone,age,bood,weight,parasitic,positive,negative)

            database

            with sqlite3.connect("donar.db") as connection:
                cursor=connection.cursor()
                cursor.execute("""

                """)
        except :
            return redirect("./signin")



if __name__=="__main__":
    app.run(port=5000,debug=True)