from flask import Flask, render_template, request, redirect, url_for, flash
from forms import ScrapeForm
import driver
import os
import pandas as pd


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

sites = ["Jumia", "Kikuu"]
state = {}


@app.route("/", methods=["GET", "POST"])
def index():
    form = ScrapeForm()

    if form.validate_on_submit():

        filename, err, errmsg = driver.main(search_str=request.form['item'], pages=int(
            request.form['page']), site=request.form['site'])

        if err:
            flash(errmsg, "danger")
            return render_template("index.html", sites=sites, form=form)

        global state
        state = {"site": request.form['site'], "item": request.form['item']}
        state["filename"] = os.path.join(ROOT_DIR, filename)
        return redirect(url_for("result"))

    return render_template("index.html", sites=sites, form=form)


@app.route("/result", methods=["GET", "PUT"])
def result():
    global state
    data = pd.read_csv(state["filename"])
    return render_template("result.html", info=state, data=data)


if __name__ == "__main__":

    app.run(debug=True)
