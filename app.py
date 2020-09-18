from flask import Flask, render_template, request
import driver
import os.path as path

ROOT_DIR = path.dirname(path.abspath(__file__))

app = Flask(__name__)

sites = ["Jumia", "Kikuu"]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", sites=sites)
    else:

        filename, err, errmsg = driver.main(search_str=request.form['item'], pages=int(
            request.form['page']), site=request.form['site'])
        data = {}
        data["file"] = path.join(ROOT_DIR, filename)
        data["error_msg"] = errmsg if err else ""
        return render_template("result.html", data=data)


if __name__ == "__main__":

    app.run(debug=True)
