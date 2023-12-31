from flask import Flask, render_template, request, redirect
from hashlib import sha1
import sqlite3
import os

app = Flask(__name__)

# ! track completion state of problems, add default False for each problem
problems = [False, False, False]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ctfvalidate", methods=["POST"])
def ctfValidate():
    code = request.form.get("code")
    id = request.form.get("id")
    print(code)
    print(os.environ.get("accCTF1"))
    if id == "0" and code == f"accCTF({os.environ.get('accCTF1')})":
        problems[0] = True
        return render_template(
            "ctf.html", message="Correct! Challenge 1 Complete!", problems=problems
        )
    if id == "1" and code == f"accCTF({os.environ.get('accCTF2')})":
        problems[1] = True
        return render_template(
            "ctf.html", message="Correct! Challenge 2 Complete!", problems=problems
        )
    if id == "2" and code == f"accCTF({os.environ.get('accCTF3')})":
        problems[2] = True
        return render_template(
            "ctf.html", message="Correct! Challenge 3 Complete!", problems=problems
        )
    return render_template(
        "ctf.html",
        message="uhoh, looks like you did something wrong... ask an officer if ur confused :)",
        problems=problems,
    )


@app.route("/ctflogin")
def ctfLogin():
    return render_template("ctflogin.html")


@app.route("/ctf", methods=["POST"])
def ctf():
    password = request.form.get("password")
    actual_password = os.environ.get("CTF_PASSWORD")
    if password == actual_password:
        return render_template("ctf.html", message="", problems=problems)
    else:
        return redirect("/ctflogin")


@app.route("/deleteuser", methods=["POST"])
def deleteUser():
    try:
        data = request.get_json()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        username = data["username"]
        cursor.execute(f"DELETE FROM users WHERE username='{username}'")
        connection.commit()
        connection.close()
        print(f"successfully deleted user {username}")
        return f"successfully deleted user: {username}"
    except:
        print("Error occurred deleting user")
        return "Error occurred deleting user"


@app.route("/adduser", methods=["POST"])
def addUser():
    try:
        data = request.get_json()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        username = data["username"]
        password = data["password"]
        cursor.execute(
            "INSERT INTO users (username, pass, manager) VALUES (?, ?, ?)",
            (username, password, False),
        )
        connection.commit()
        connection.close()
        print(f"successfully added user {username}")
        return f"successfully added user: {username}"
    except:
        print("Error occurred adding user")
        return "Error occurred adding user"


@app.route("/dashboard", methods=["POST"])
def dashboard():
    username = request.form.get("username")
    password = request.form.get("password")
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    try:
        testCheckManager = connection.execute(
            f"SELECT * FROM users WHERE username='{username}' AND pass='{password}' AND manager=1 LIMIT 1"
        ).fetchone()
        testCheckManager = testCheckManager["manager"]
    except Exception as e:
        print("Error occurred:", e)
        testCheckManager = False

    if testCheckManager:
        users = connection.execute("SELECT * FROM users").fetchall()
        userData = []
        for user in users:
            userData.append(
                {
                    "username": user["username"],
                    "pass": sha1(user["pass"].encode()).hexdigest(),
                }
            )
        return render_template("dashboard.html", users=userData)
    else:
        return redirect("/")


if __name__ == "__main__":
    # ! set debug mode to false on production
    app.run(debug=True)
