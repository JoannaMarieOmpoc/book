from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, IntegerField, ValidationError
from wtforms.validators import DataRequired
from sqlalchemy import func, or_, and_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:yowanna1997@127.0.0.1:5432/ojt'
db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'flaskimplement'

class Records(db.Model):
    __tablename__ = "records"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, year):
        self.title = title
        self.author= author
        self.year = year

    def __repr__(self):
        return '<title {}>'.format(self.title)

class RecordsForm(Form):
    title = StringField('Book Title', validators=[DataRequired()])
    author = StringField('Book Author', validators=[DataRequired()])
    year = IntegerField('Published Year', validators=[DataRequired()])

class SearchForm(Form):
    search = StringField('', validators=[DataRequired()])

db.create_all()
app.debug = True

@app.route('/', methods=['GET','POST'])
def records():
    form = SearchForm()
    result1 = Records.query.order_by(Records.year)
    if request.method == 'POST':
        if form.validate_on_submit():
            if Records.query.filter_by(title=form.search.data).first():
                result = Records.query.order_by(Records.year).filter_by(title=form.search.data)
                return render_template('result.html', records=result, form=form)

            elif Records.query.filter_by(author=form.search.data).first():
                result = Records.query.filter_by(author=form.search.data)
                return render_template('result.html', records=result, form=form)

            elif Records.query.filter_by(year=form.search.data).first():
                result = Records.query.filter_by(year=form.search.data)
                return render_template('result.html', records=result, form=form)

            else:
                return render_template('result.html', records=result1, form=form)
    else:
        return render_template('records.html', records=result1, form=form)
    return render_template('records.html', records=result1, form=form)

@app.route('/add', methods=['POST','GET'])
def addrecords():
    form = RecordsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            records = Records(title=form.title.data,
                              author=form.author.data,
                              year=form.year.data)
            db.session.add(records)
            db.session.commit()
            result = Records.query.order_by(Records.year)
            form1=SearchForm()
            return render_template('records.html', records=result, form=form1)
    return render_template('addrecords.html', form=form)

@app.route('/edit/<id>', methods=['POST', 'GET'])
def editrecords(id):
    records = Records.query.filter_by(id=id).first()
    form = RecordsForm()
    if form.validate_on_submit():
        records.title = form.title.data
        records.author = form.author.data
        records.year = form.year.data
        db.session.add(records)
        db.session.commit()
        result = Records.query.order_by(Records.year)
        form1 = SearchForm()
        return render_template('records.html', records=result, form=form1)
    else:
        form.title.data = records.title
        form.author.data = records.author
        form.year.data = records.year
    return render_template('addrecords.html', form=form)

@app.route('/delete/<id>', methods=['GET','POST'])
def remove(id):
    result = Records.query.filter_by(id=id).first()
    db.session.delete(result)
    db.session.commit()
    records = Records.query.order_by(Records.year)
    form=SearchForm()
    return render_template('records.html', records=records, form=form)

if __name__ == '__main__':
    app.run()
