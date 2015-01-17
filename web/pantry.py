from flask import Flask, url_for, render_template, request, redirect, session, abort, flash, g

app = Flask(__name__)
app.config.from_object(__name__)

# App settings
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='pantry key',
))

@app.route("/")
def pantry():
    return render_template('home.html')

@app.route("/examples")
def examples():
    return render_template('examples.html')

@app.route("/register")
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run()
