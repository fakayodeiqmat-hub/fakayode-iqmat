import os
import mysql.connector
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get("CSC312_DB_PASSWORD"),
        database="csc312_db"
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        password_hash = generate_password_hash(password)
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
    "INSERT INTO tbl_user (username, password) VALUES (%s, %s)",
    (username, password_hash)
)
            connection.commit()
            message = f"Signup successful for {username}"

        except mysql.connector.IntegrityError:
            message = "That username already exists. Please choose another."

        finally:
            cursor.close()
            connection.close()

        return message

    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)