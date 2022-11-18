from flask import Flask,render_template,redirect,url_for,request,make_response,flash
import sqlite3 as sql
import jwt
import uuid
from datetime import datetime, timedelta
import ibm_db
from markupsafe import escape
import uuid

conn=ibm_db.connect("",'','')



import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
# Instantiate the client\
SID_KEY = ''
# Define the campaign settings\
subject= "Plasma",
sender={"email":"","name":"My-Plasma"}

type= "classic",
# Content that will be sent\
html_content= '<html><body><h3> An account is created using the following email </h3><p> the <a > link </a></p></body></html>'
# Select the recipients\



def sendinblue(SID_KEY,SID_SENDER,receiver,subject,html_content):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = SID_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = subject
    sender = SID_SENDER
    replyTo = SID_SENDER
    html_content = html_content
    to = receiver
    params = {"parameter":"My param value","subject":"New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to,  reply_to=replyTo,html_content=html_content, sender=sender, subject=subject)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
subject="Congratulations You have created your account Please verify your account "



def verify(token):
    
    data = jwt.decode(token, "Hello", algorithms='HS256')
    
    return data["email"]



app=Flask(__name__,static_folder="static")

@app.route("/")
def reload():
    return redirect("/home")

@app.route("/home")
def homeFun():
    try:

        token = request.cookies.get('token')
        email = verify(token)
        return render_template("./home.html")
    except: 
        flash("Something Went Wrong","alert alert-danger")
        return redirect("/signin")
@app.route("/signin",methods=["POST","GET"])
def signin():
    if request.method=="GET":
        return render_template("signin.html")
    else:
        
        email=request.form["email"]
        password=request.form["password"]
        print(email,password)

        sql=f""" SELECT  email,password FROM DONAR WHERE email='{escape(email)}'"""
        stmt=ibm_db.exec_immediate(conn,sql)
        donar=ibm_db.fetch_tuple(stmt)
    
        print(donar)

        
        if donar==None:
            flash("No matching results",'alert alert-danger')
            redirect("/signin")
        else:
            token = jwt.encode({"email": email, 'exp': datetime.utcnow(
            )+timedelta(minutes=900)}, "Hello", algorithm='HS256')
            print(token)
            response = make_response(
                redirect("/home"))
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
            
            
            sql="INSERT INTO DONAR (id,name,email,phone,password) VALUES (?,?,?,?,?)"
            prep_stmt=ibm_db.prepare(conn,sql)

            ibm_db.bind_param(prep_stmt,1,key)
            ibm_db.bind_param(prep_stmt,2,name)
            ibm_db.bind_param(prep_stmt,3,email)
            ibm_db.bind_param(prep_stmt,4,phone)
            ibm_db.bind_param(prep_stmt,5,password)
            ibm_db.execute(prep_stmt)
            flash("Successfully Created","alert alert-success")
            return redirect("/home")

        else:
            flash("Something Went Wrong","alert alert-danger")
            return redirect("/signup")

@app.route("/signout")
def logout():
    response = make_response(render_template("./signin.html"))
    response.set_cookie('token', '')
    flash("logged out successfully")
    return response

@app.route("/home")
def home():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        print(email)
        return render_template("./home.html")
    except:
        flash("Something Went Wrong","alert alert-danger")
        return redirect("./signin")

@app.route("/profile")
def profile():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        sql=f""" SELECT name,phone FROM DONAR WHERE email='{escape(email)}' """
        stmt=ibm_db.exec_immediate(conn,sql)
        data=ibm_db.fetch_assoc(stmt)
        print(email)
        return render_template("./profile.html",data=data)
    except:
        flash("Something Went Wrong","alert alert-danger")
        return redirect("./signin")

@app.route("/plasma-request",methods=("GET","POST"))
def plasma():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        if request.method=='GET':

            return render_template("./plasma.html")
        else:
            name=request.form["name"]
            age=request.form["age"]
            gender=request.form["gender"]
            blood_group=request.form['blood_group']
            phone=request.form['phone']
            email=request.form['email']
            address=request.form['address']
            key = uuid.uuid1().hex
            print(name,age,gender,blood_group,phone,email,address)

            sql=""" INSERT INTO PLASMA_REQUEST (name,phone,age,blood_group,gender,email,address,id) VALUES (?,?,?,?,?,?,?,?) """
            prep_stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(prep_stmt,1,name)
            ibm_db.bind_param(prep_stmt,2,phone)
            ibm_db.bind_param(prep_stmt,3,age)
            ibm_db.bind_param(prep_stmt,4,blood_group)
            ibm_db.bind_param(prep_stmt,5,gender)
            ibm_db.bind_param(prep_stmt,6,email)
            ibm_db.bind_param(prep_stmt,7,address)
            ibm_db.bind_param(prep_stmt,8,key)

            ibm_db.execute(prep_stmt)
            sql=""" SELECT blood_group,email FROM DONARLIST """
            stmt=ibm_db.exec_immediate(conn,sql)
            data=ibm_db.fetch_assoc(stmt)
            Total_lis=[]
            while data !=False:
                Total_lis.append(data)
                data=ibm_db.fetch_assoc(stmt)
            match=[]
            print(match)
            for x in Total_lis:
                if x["BLOOD_GROUP"].upper() ==blood_group.upper():
                    if x["EMAIL"] != None:
                            match.append({"email":x["EMAIL"]})

            receiver=Total_lis.reverse()
            print(match)
            subject="You Have a request for Plasma"
            html_content='<html><body><h3>  {} is requesting for Plasma <p> Please send your response within 6 hours to avoid immediate casualities </p>  </h3><p>Contact {}</p> <p>Phone: {} </p> <p>Email:{}</p></body></html>'	.format(name,name,phone,email)
            sendinblue(SID_KEY,sender,match,subject,html_content)
            print("MAil sent")
            flash("Successfully Submitted","alert alert-success")


            return redirect("/home")
            
            

    except Exception as e:
        flash("Something Went Wrong","alert alert-danger")
        print(e)
        return redirect("/signin")


@app.route("/donar-list",methods=("GET","POST"))
def donar_list():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        if request.method=="GET":
        
            sql=""" SELECT name,age,blood_group,gender,phone,email,id  FROM DONARLIST """
            stmt=ibm_db.exec_immediate(conn,sql)
            data=ibm_db.fetch_assoc(stmt)
            donar_list=[]
            while data != False:
              donar_list.append(data)
              data = ibm_db.fetch_both(stmt)
            donar_list.reverse()
            return render_template("./donar-list.html",data=donar_list)

    except  Exception as e:
        print(e)
        flash("Something Went Wrong","alert alert-danger")
        return redirect("/signin")

@app.route("/view/<id>",methods=("GET","POST"))
def viwDonorInfo(id):
    try:
        token = request.cookies.get('token')
        email = verify(token)
        if request.method=="GET":
            sql=f""" SELECT * FROM DONARLIST WHERE id='{escape(id)}'  """
            stmt=ibm_db.exec_immediate(conn,sql)
            user=ibm_db.fetch_assoc(stmt)
            print(user)
            return render_template("view.html",data=user)
        

    except Exception as e:
        flash("Something Went Wrong","alert alert-danger")
        print(e)
        
        return redirect("/signin")



@app.route("/plasma-requests")
def plasma_request():
    try:
        token = request.cookies.get('token')
        email = verify(token)
        donar_list=[]
        sql=""" SELECT * FROM PLASMA_REQUEST  """
        stmt=ibm_db.exec_immediate(conn,sql)
        data=ibm_db.fetch_assoc(stmt)
        print(donar_list)
        while data != False:
              donar_list.append(data)
              data = ibm_db.fetch_both(stmt)

        return render_template("request.html",data=donar_list)
    

    except Exception as e:
        flash("Something Went Wrong","alert alert-danger")
        print(e)
        return redirect("/signin")






@app.route("/donar-registration",methods=["POST","GET"])
def donar_registration():
    if request.method=="GET":

        try:
            token = request.cookies.get('token')
            email = verify(token)
            print(email)
            return render_template("./donar.html")

        except:
            flash("Something Went Wrong","alert alert-danger")
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
            hiv=request.form["hiv"]
            disease=request.form["disease"]
            drugs=request.form["drugs"]
            vaccine=request.form["vaccine"]
            health=request.form["health"]
            donated=request.form["donated"]
            date=request.form["date"]
            gender=request.form["gender"]
            email=request.form["email"]
            key = uuid.uuid1().hex

            print(name,phone,age,blood,weight,parasitic,hiv,disease,drugs,vaccine,donated,date,health)

            #database
            sql=""" INSERT INTO DONARLIST (name,phone,age,blood_group,weight,infection,hiv,blood_disease,drugs,vaccine,donated_pls,date,health,id,gender,email) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
            prep_stmt=ibm_db.prepare(conn,sql)
            ibm_db.bind_param(prep_stmt,1,name)
            ibm_db.bind_param(prep_stmt,2,phone)
            ibm_db.bind_param(prep_stmt,3,age)
            ibm_db.bind_param(prep_stmt,4,blood)
            ibm_db.bind_param(prep_stmt,5,weight)
            ibm_db.bind_param(prep_stmt,6,parasitic)
            ibm_db.bind_param(prep_stmt,7,hiv)
            ibm_db.bind_param(prep_stmt,8,disease)
            ibm_db.bind_param(prep_stmt,9,drugs)
            ibm_db.bind_param(prep_stmt,10,vaccine)
            ibm_db.bind_param(prep_stmt,11,donated)
            ibm_db.bind_param(prep_stmt,12,date)
            ibm_db.bind_param(prep_stmt,13,health)
            ibm_db.bind_param(prep_stmt,14,key) 
            ibm_db.bind_param(prep_stmt,15,gender)
            ibm_db.bind_param(prep_stmt,16,email)    

            ibm_db.execute(prep_stmt)
            sql=""" SELECT blood_group,email FROM PLASMA_REQUEST """
            stmt=ibm_db.exec_immediate(conn,sql)
            data=ibm_db.fetch_assoc(stmt)
            Total_lis=[]
            while data !=False:
                Total_lis.append(data)
                data=ibm_db.fetch_assoc(stmt)
            match=[]
            print(match)
            for x in Total_lis:
                if x["BLOOD_GROUP"].upper() ==blood.upper():
                    if x["EMAIL"] != None:
                            match.append({"email":x["EMAIL"]})

            receiver=Total_lis.reverse()
            print(match)
            subject="You Have a request for Plasma"
            html_content='<html><body><h3>  {} is donating his Plasma <p> Contact him for the uppercomming updates </p>  </h3><p>Contact {}</p> <p>Phone: {} </p> <p>Email:{}</p></body></html>'	.format(name,name,phone,email)
            sendinblue(SID_KEY,sender,match,subject,html_content)
            print("MAil sent")
            flash("Successfully Submitted","alert alert-success")




            return redirect("/donar-list")


                
        except Exception as e:
            flash("Something Went Wrong","alert alert-danger")
            print(e)
            return redirect("./home")

@app.route("/mail/<id>")
def mailhim(id):
    try:
        token = request.cookies.get('token')
        email = verify(token)
        sql=f""" SELECT id,email,name FROM DONARLIST WHERE id='{escape(id)}' """
        stmt=ibm_db.exec_immediate(conn,sql)
        receiptent=ibm_db.fetch_assoc(stmt)
        sql=f""" SELECT name,phone,email FROM DONAR WHERE email='{escape(email)}' """
        stmt=ibm_db.exec_immediate(conn,sql)
        sender_info=ibm_db.fetch_assoc(stmt)
        print(receiptent,sender_info)
        if receiptent != False and sender_info != False :

            receiver=[{"email":receiptent["EMAIL"],"name":receiptent["NAME"]}]
            subject="You Have a request for Plasma"
            html_content='<html><body><h3> An {} is requesting for Plasma <p> Please send your response within 6 hours to avoid immediate casualities </p>  </h3><p>Contact User</p> <p>Phone: {} </p> <p>Email:{}</p></body></html>'	.format(sender_info["NAME"],sender_info["PHONE"],sender_info["EMAIL"])
            sendinblue(SID_KEY,{"name":"My-Plasma","email":"devvijaya959@gmail.com"},receiver,subject,html_content)
            print("MAil sent")
            return redirect("/donar-list")

        flash("Successfully Mailed","alert alert-success")
        return redirect("/home")
    except Exception as e:
        print(e)
        flash("Something Went Wrong","alert alert-danger")
        return redirect("/signin")




if __name__=="__main__":
    app.run(port=5000,debug=True)