from flask import Flask, render_template, request
from forms import ScrapeForm
import driver
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

sites = ["Jumia", "Kikuu"]


@app.route("/", methods=["GET", "POST"])
def index():
    form = ScrapeForm()

    if form.validate_on_submit():

        filename, err, errmsg = driver.main(search_str=request.form['item'], pages=int(
            request.form['page']), site=request.form['site'])
        data = {}
        data["file"] = os.path.join(ROOT_DIR, filename)
        data["error_msg"] = errmsg if err else ""
        return render_template("result.html", data=data)
    return render_template("index.html", sites=sites, form=form)


if __name__ == "__main__":

    app.run(debug=True)
