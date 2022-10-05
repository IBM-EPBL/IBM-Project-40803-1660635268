from flask import Flask, render_template, url_for, request, redirect
import sqlite3 as sql

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/signin")
def signin():
    return render_template('signin.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        val = request.form
        print(val["name"])
        return redirect("/")
    else:
        return render_template('signup.html')


@app.route("/add", methods=["GET", "POST"])
def additem():
    if request.method == "GET":
        return render_template('addpage.html')
    else:
        uname = request.form["username"]
        mobile = request.form["mobile"]
        with sql.connect("user.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO students (name,mobile) VALUES (?,?)", (uname, mobile))
            connection.commit()

    
        return redirect("/item")


@app.route("/item")
def item():
    with sql.connect("user.db") as connection:
        connection.row_factory = sql.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        users = cursor.fetchall()
        # print(users)

    return render_template("item.html", user=users)


@app.route("/edit/<key>", methods=["GET", "POST"])
def editroute(key):
    if request.method == "GET":
        with sql.connect("user.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students WHERE name==? ", (key,))
            user = cursor.fetchone()
            print(user)
            return render_template("addpage.html", item=user)
    else:
        uname = request.form['username']
        mobile = request.form['contact']
        with sql.connect("user.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE students SET name=?,mobile=? WHERE name=?", (uname, mobile, key,))
            connection.commit()
            return redirect("/item")


@app.route("/delete/<name>")
def deleteRoute(name):
    with sql.connect("user.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE name=?", (name,))
        return redirect("/item")