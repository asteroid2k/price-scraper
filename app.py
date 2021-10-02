from flask import Flask, render_template, request, redirect, url_for, session
from forms import ScrapeForm, DataframeForm
import driver
import os
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
# app key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Global variables
sites = ["Jumia", "Kikuu"]

# Custom Filters


@app.template_filter('splitstr')
def splitstr(str, index, char):
    return str.split(char)[index]

# ROUTES

# homepage


@app.route("/", methods=["GET", "POST"])
def index():
    # initialize form
    form = ScrapeForm()

    # POST method
    if form.validate_on_submit():

        # run scraping program with argument values from  Form
        filename, err, errmsg = driver.main(search_str=request.form["item"], pages=int(
            request.form["page"]), site=request.form["site"])

        # render hompage with errors if any
        if err:
            print(f"ERROR: {errmsg}")
            return render_template("index.html", sites=sites, form=form)

        state = {"site": request.form["site"], "item": request.form["item"]}
        state["filename"] = os.path.join(ROOT_DIR, filename)
        session["info"] = state
        # redirect to results page if no errors occur
        return redirect(url_for("result"))

    # GET method return homepage

    return render_template("index.html", sites=sites, form=form)

# Scrape Result


@app.route("/result", methods=["GET", "POST"])
def result():
    form = DataframeForm()
    err, err_msg = True, ""
    dataframe = {}
    info = {}

    if "info" in session:
        err = False
        info = session["info"]
    else:
        err_msg = "No Data"

    # POST method
    if form.validate_on_submit():
        err, err_msg, dataframe, info = driver.filter_results(
            filename=info["filename"], qfilter=request.form["operator"], value=request.form["value"], param=request.form["param"], info=info)
        if err:
            print(f"ERROR:{err_msg}")
        return render_template("result.html", error=err, error_msg=err_msg, info=info, form=form, df=dataframe.itertuples())
# GET method
    err, err_msg, dataframe, info = driver.filter_results(
        filename=info["filename"], qfilter="", value="", param="", info=info)
    if err:
        print(f"ERROR:{err_msg}")
    return render_template("result.html", error=err, error_msg=err_msg, info=info, form=form, df=dataframe.itertuples())


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
