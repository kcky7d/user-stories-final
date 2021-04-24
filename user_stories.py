from flask import Flask, render_template, request, redirect, url_for, g, flash, Markup, session
from flask_wtf import FlaskForm
from flask_table import Table, Col, ButtonCol
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DecimalField, validators
from wtforms.validators import InputRequired, DataRequired, Length
from wtforms.fields.html5 import EmailField
import pdb
import sqlite3
import string

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"

class SortableTable(Table):

    id = Col('ID')
    tool = Col('Tool')
    work_role = Col('Work Role')
    user_story = Col('User Story', allow_sort=False)
    vote = ButtonCol('Vote', 'vote_submit', text_fallback='Vote',allow_sort=False)
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'

        return url_for('previous_submissions', sort=col_key, direction=direction)

class Item(object):
    def __init__(self, id, tool, work_role, user_story):
        self.id = int(id)
        self.tool = tool
        self.work_role = work_role
        self.user_story = user_story

    @classmethod
    def get_elements(cls, user_stories):
        element_list = []

        for story in user_stories:
            element_list.append(Item(story['id'], story['tool'],
                                story['work_role'], story['user_story']))
        return element_list    

    @classmethod
    def get_sorted_by(cls, user_stories, sort, reverse=False):
        return sorted(
            cls.get_elements(user_stories),
            key=lambda x: getattr(x, sort),
            reverse=reverse)


class NewSubmissionForm(FlaskForm):
    tool        = SelectField("Tool")
    work_role   = SelectField("Work Role")
    feature     = TextAreaField("Feature", 
                        validators=[InputRequired("Input is required"),
                                    DataRequired("Data is required"),
                                    Length(min=10, max=100, message="Must be between 10 and 100 characters")],
                                    render_kw={"placeholder": "describe the feature"})
    rationale   = TextAreaField("Rationale", 
                        validators=[InputRequired("Input is required"),
                                    DataRequired("Data is required"),
                                    Length(min=10, max=100, message="Must be between 10 and 100 characters")],
                                    render_kw={"placeholder": "describe how this will help you"})
    submit      = SubmitField("Submit")


class FilterForm(FlaskForm):
    tool        = SelectField("Tool")
    work_role   = SelectField("Work Role")    
    submit      = SubmitField("Filter")



class ContactForm(FlaskForm):
    first_name  = TextAreaField("First Name", 
                        validators=[InputRequired("Input is required"),
                                    DataRequired("Data is required")])
    last_name   = TextAreaField("Last Name", 
                        validators=[InputRequired("Input is required"),
                                    DataRequired("Data is required")])
    email       = EmailField("Email Address", [validators.DataRequired(), validators.Email()])

    message     = TextAreaField("Message", 
                        validators=[InputRequired("Input is required"),
                                    DataRequired("Data is required"),
                                    Length(min=10, max=100, message="Must be between 10 and 100 characters")],
                                    render_kw={"placeholder": "Message must be between 10 and 100 characters"})
    submit      = SubmitField("Submit")


def strip_punctuation(input):
    input = input.translate(str.maketrans('','',string.punctuation))
    return input


@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/about_user_stories")
def about_user_stories():
    return render_template("about_user_stories.html")

@app.route("/new_submission", methods=["GET", "POST"])
def new_submission():
    conn = get_db()
    c = conn.cursor()
    form = NewSubmissionForm()

    c.execute("SELECT name, name FROM tools")
    tools = c.fetchall()

    # [(1, 'Awesome Tool'), (2, 'Great Tool'), (3, 'Horrible Tool')]
    form.tool.choices = tools

    c.execute("SELECT name, name FROM work_roles")
    work_roles = c.fetchall()

    # [(1, 'analyst'), (2, 'executive assistant'), (3, 'data scientist'), (4, 'program manager')]
    form.work_role.choices = work_roles

    if form.validate_on_submit():
        tool        = form.tool.data
        work_role   = form.work_role.data
        feature     = strip_punctuation(form.feature.data).lower()
        rationale   = strip_punctuation(form.rationale.data).lower()

        user_story = 'As a {}, I need {}, so that {}.'.format(work_role, feature, rationale)

        c.execute("""INSERT INTO user_stories (tool, work_role, user_story)
                        VALUES(?,?,?)""",
                        (
                            tool,
                            work_role,
                            user_story                        
                        )                        
        )
        conn.commit()
        flash("Your submission: {} has been successfully submitted.".format(user_story), "success")
        return redirect(url_for("contact_form"))
    if form.errors:
        flash("{}".format(form.errors), "danger")
    return render_template("new_submission.html", form=form)

@app.route("/previous_submissions", methods=["GET", "POST"])
def previous_submissions():
    conn = get_db()
    c = conn.cursor()

    form = FilterForm(request.args, meta={"csrf":False})
   
    c.execute("SELECT name, name FROM tools")
    tools = c.fetchall()
    tools.insert(0, ("---", "---"))
    form.tool.choices = tools

    c.execute("SELECT name, name FROM work_roles")
    work_roles = c.fetchall()
    work_roles.insert(0, ("---", "---"))
    form.work_role.choices = work_roles

    query = """SELECT
                    id, tool, work_role, user_story 
                    FROM user_stories
    """

    
    if form.validate():
        filter_queries  = []
        parameters      = []

        if form.tool.data != '---':
            filter_queries.append("tool LIKE ?")
            parameters.append("%" + form.tool.data + "%")
        
        if form.work_role.data != '---':
            filter_queries.append("work_role LIKE ?")
            parameters.append("%" + form.work_role.data + "%")

        if filter_queries:
            query += " WHERE "
            query += " AND ".join(filter_queries)

        us_from_db = c.execute(query, tuple(parameters))

    else:
        us_from_db = c.execute(query + "ORDER BY id DESC")


    user_stories = []
    for row in us_from_db:
        entry = {
            "id": row[0],
            "tool": row[1],
            "work_role": row[2],
            "user_story": row[3]
        }
        user_stories.append(entry)

    sort = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')
    table = SortableTable(Item.get_sorted_by(user_stories,sort, reverse),
                                                sort_by=sort,
                                                sort_reverse=reverse)
    table_html = Markup(table.__html__())



    return render_template("previous_submissions.html", table_html=table_html, form=form)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact_form", methods=["GET", "POST"])
def contact_form():
    if request.method == "POST":
        form = ContactForm(meta={"csrf":False})
        if form.validate_on_submit():
            first_name        = form.first_name.data
            flash("Thank you for your input, {}. A member of our team will be in contact shortly".format(first_name), "success")
            return redirect(url_for("welcome"))    
        if form.errors:           
            flash("{}".format(form.errors), "danger")
        return render_template("contact_form.html", form=form)

    else:
        form = ContactForm(meta={"csrf":False})
        return render_template("contact_form.html", form=form)

@app.route("/vote_success", methods=["GET", "POST"])
def vote_submit():
    flash("Your vote has been submitted!","success")
    return redirect(url_for("contact_form"))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('db/user_stories.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

