from flask import (Flask, render_template, session, redirect, url_for, flash,
                   request)
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


def is_uoft_email(email):
    return email is not None and 'utoronto' in email


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email address?',
                       validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        if is_uoft_email(form.email.data):
            return redirect(url_for('chatbot'))
        return redirect(url_for('index'))
    email = session.get('email')
    return render_template('index.html', form=form, name=session.get('name'),
                           email=email, is_uoft=is_uoft_email(email))


@app.route('/chatbot')
def chatbot():
    # Only users who submitted a name and a valid UofT email can chat
    if not is_uoft_email(session.get('email')):
        return redirect(url_for('index'))
    return render_template('chat.html', name=session.get('name'))


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    text = message.lower()

    if 'my name is' in text:
        # Remember the name in the session so later requests can use it
        start = text.index('my name is') + len('my name is')
        chat_name = message[start:].strip(' .!?')
        session['chat_name'] = chat_name
        reply = 'Nice to meet you, {}!'.format(chat_name)
    elif 'what is my name' in text:
        if 'chat_name' in session:
            reply = 'Your name is {}.'.format(session['chat_name'])
        else:
            reply = "I don't know your name yet. Tell me by saying 'My name is ...'."
    elif 'hello' in text:
        reply = 'Hello!'
    else:
        reply = "I don't understand."

    return {'reply': reply}


if __name__ == '__main__':
    app.run(debug=True)
