from flask import Flask,render_template,request,redirect
import sqlite3 as sql

app=Flask(__name__,static_folder="static")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/about')
def aboutpage():
    return render_template('about.html')

#database connection    

@app.route('/signup', methods=['POST','GET'])
def submitpage():
    if(request.method =='POST'):
        try:
            name=request.form['name'];
            email=request.form['email'];
            phone=request.form['phone'];
            password=request.form['password'];
            

            with sql.connect("lists.db") as con:
                
                cur=con.cursor();
                cur.execute("INSERT INTO lists (name,email,phone,password) VALUES (?,?,?,?)",(name,email,phone,password))
                con.commit()
                msg="Successfully added..!!";
            return msg
        
        except:
            con.rollback();
            msg="error in adding";
        finally:
            return redirect("/lists")
            con.close();



@app.route("/lists")
def lists():
    with sql.connect("lists.db") as con:
        
        con.row_factory=sql.Row

        
        cur=con.cursor()
        cur.execute("SELECT * FROM lists")
        users=cur.fetchall();
        print(users)
    return render_template("lists.html",users=users)


@app.route("/edit/<name>")
def edit(name):
    
    with sql.connect("lists.db") as con:
        cur=con.cursor()
        cur.execute("SELECT * FROM lists WHERE name=?",(name,))
        user=cur.fetchone();
        print(user)
    return render_template("update.html",user=user )

        
        

@app.route("/delete/<name>")
def delete(name):
    with sql.connect("lists.db") as con:
        cur=con.cursor()
        cur.execute("DELETE  FROM lists WHERE name=?",(name,))
        return redirect("/lists")
        

@app.route("/edit/<names>",methods=['POST'])
def update(names):
    name=request.form['name'];
    email=request.form['email'];
    phone=request.form['phone'];
    with sql.connect("lists.db") as con:
        cur=con.cursor()
        cur.execute("UPDATE lists SET name=?,email=?,phone=? WHERE name=?",(name,email,phone,names))
        con.commit()
    return redirect("/lists")
    
    

if __name__=='__main__': 
    app.run(debug=True)