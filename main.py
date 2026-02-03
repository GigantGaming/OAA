from flask import Flask, render_template, request, redirect, session, url_for, make_response
from github_db import register_user, login_user

app = Flask(__name__)
app.secret_key = "super5654_secret_key1220"   # session ke liye

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
    

@app.route("/")
def home():
  user = session.get("user")
  return render_template("home.html", user=user)

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        success, user = login_user(
            request.form["email"],
            request.form["password"]
        )

        if success:
            session.clear()   # 🟢 OLD DATA CLEAR
            del user["password"]
            session["user"] = user
            return redirect("/dashboard")
        else:
            message = "Invalid email or password"

    return render_template("login.html", message=message)
  

@app.route("/register", methods=["GET", "POST"])
def register():
  msg = ""
  if request.method == "POST":
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    success, msg = register_user(username, email, password)
    if success:
            return redirect(url_for("login"))


  return render_template("register.html", message=msg)


# ---------------- DASHBOARD (PRIVATE) ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("profile.html", user=session["user"])
    

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
  app.run(debug=True)
