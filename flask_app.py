import os

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "listItems.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class itemList(db.Model):
    id = db.Column(db.Integer, primary_key = True) #primary key column, automatically generated IDs
    user = db.Column(db.String(20), index = True, unique = False)
    item = db.Column(db.String(20), index = True, unique = False)
    note = db.Column(db.String(50), index = True, unique = False)

    def __repr__(self):
        return "Item: {}, {} posted by {}".format(self.item, self.note, self.user)

@app.route('/', methods=["GET", "POST"])
@app.route('/<name>')
def home(name=None):
    if name and name != 'None':
        name = name.lower()
        items = itemList.query.filter(itemList.user == name)
    else:
        items = itemList.query.all()

    return render_template('index.html', name=name, items=items)

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("user")
    if request.form:
        newItem = itemList(user=request.form.get('user'),item=request.form.get('item'), note=request.form.get('note'))
        db.session.add(newItem)
        db.session.commit()
    
    if (name and name != "None"):
        return redirect("/{}".format(name))
    else:
        return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    item = request.form.get("item")
    name = request.form.get("user")
    deletedItem = itemList.query.filter_by(item=item).first()
    db.session.delete(deletedItem)
    db.session.commit()

    if (name and name != "None"):
        return redirect("/{}".format(name))
    else:
        return redirect("/")

if __name__ == '__main__':
    app.run(debug = True)