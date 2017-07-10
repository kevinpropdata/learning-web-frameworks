from flask import Flask, request, session, redirect

# ===================================================================== #
# Initialize our application server
# ===================================================================== #
app = Flask(__name__)

# a security token - unique key to our app to ensure secure sessions
app.secret_key = "3434rkjfsdkljsdf423;203040-42309sdjk"

# ===================================================================== #


# ===================================================================== #
# custom helper functions
# ===================================================================== #

# takes in a template path and substitues placehoders with relevant values
def build_template(template, template_placeholders):
    '''
        the template variable will contain just the template
        name not it's full path , since all templates are stored
        in html/ and have an extension of .html , we need not
        repeat these throughout our app; rather we prepend
        the template variable with html and append .html to
        generate the full path to our template :
        e.g. index becomes html/index.html
             about becomes html/about.html
    '''
    tpl_path = "html/%s.html" % template

    # now open the template file and store it's contents as a string
    # in template_data.
    template_data = open(tpl_path, "r").read()

    '''
        run through all the placeholder variables stored in
        template_placeholders and substitute the placeholders
        with thier actual values.
    '''

    for placeholder, data in template_placeholders.items():
        template_data = template_data.replace('{{%s}}' % placeholder, data)

    # finally returned the final string with the subsituted values
    return template_data


# =================================================================== #


# =================================================================== #
# various html pages based on the url
# =================================================================== #


# =================================================================== #
# serving up a basic html homepage
# =================================================================== #


@app.route("/")
def startpage():
    template_placeholders = {
        'title': "Welcome!",    # placeholder => {{title}}
        'name': 'Kevin Naidoo'  # placeholder => {{name}}
    }

    return build_template('index', template_placeholders)


# =================================================================== #
# showing a form
# =================================================================== #
@app.route("/form")
def hello_form_generator():
    template_placeholders = {"title": "Generate Hello Message"}
    return build_template('form', template_placeholders)


# =================================================================== #
# handling the form data posted to page
# =================================================================== #

@app.route("/generate", methods=["POST"])
def generated_message():
    # get the firstname and surname from our form data
    firstname = request.form['firstname']
    surname = request.form['surname']

    # add the name placeholder with our firstname, surname sent from form
    template_placeholders = {
        "title": "Generate Hello Message",
        "name": "%s %s" % (firstname, surname)
    }

    return build_template('index', template_placeholders)


# =================================================================== #
# dealing with sesisons
# =================================================================== #

# this route shows a login form
@app.route("/login")
def show_login_form():

    # message is used to show errors - in this case we have no errors
    # hence why msg is blank.
    template_placeholders = {
        "title": "Login Form",
        "msg": ""
    }
    return build_template('login_form', template_placeholders)


# this route occurs when the form is sent to the server
# upon which - the username and password will be checked
@app.route("/authenticate", methods=['POST'])
def authenticate():
    print request.form['username'], request.form['password']
    # if both the username and password match
    # start a session
    # "Login the user in" and send them to the members area
    if (
        request.form['username'] == 'kevin' and
        request.form['password'] == 'kevin'
    ):

        session['user_id'] = 1234
        return redirect("/members")
    else:
        # should the login creds not work show an error message
        # and the form again
        template_placeholders = {
            "title": "Login Form",
            "msg": "<strong>Sorry - your login details are incorrect.</strong>"
        }
        return build_template("login_form", template_placeholders)


# if the user is logged in - they'll be able to view this page
# otherwise - they are shown a login page
@app.route("/members")
def member_dashboard():
    if 'user_id' in session:
        template_placeholders = {"title": "Welcome Member!"}
        return build_template("members", template_placeholders)

    template_placeholders = {
        "title": "Login Form",
        "msg": "<strong>Sorry - you need to be logged in to view this page</strong>"
    }
    return build_template("login_form", template_placeholders)
