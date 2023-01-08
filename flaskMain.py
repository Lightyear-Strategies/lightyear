from flask import render_template, session, request
from flask_login import login_required
from flask_app.scripts.create_flask_app import app, mp
from flask_app.scripts.EmailValidator import ev_flask_functions as ev_f_f
from flask_app.scripts.PeriodicWriters import topic_tracker as t_t
from flask_app.scripts.PeriodicWriters import journalist_tracker as j_t
from flask_app.scripts.HaroTable import haro_table_functions as h_t_f
from flask_app.scripts.ContactUs import contact_us as c_u
from flask_app.scripts.LoginSignUp import auth
from flask_app.scripts import error_pages as e_p
from flask_app.scripts.config import Config
from datetime import datetime


app.add_url_rule('/email_validator', view_func=ev_f_f.email_validator, methods=['GET','POST'])
app.add_url_rule('/topic_tracker', view_func=t_t.receive_category, methods=['GET','POST'])
# app.add_url_rule('/unsubscribe_topic/<token>', view_func=t_t.unsubscribe_topic, methods=['GET','POST'], endpoint='unsubscribe_topic')

app.add_url_rule('/journalist_tracker', view_func=j_t.receive_journalists, methods=['GET','POST'])
app.add_url_rule('/unsubscribe_journalist/<token>', view_func=j_t.unsubscribe_journalist, methods=['GET','POST'], endpoint='unsubscribe_journalist')

app.add_url_rule('/query_db', view_func=h_t_f.show_haro_table, methods=['GET'])
app.add_url_rule('/api/serveHaros', view_func=h_t_f.serve_data, methods=['GET','POST'])
app.add_url_rule('/api/serveHaros/<option>', view_func=h_t_f.serve_data, methods=['GET','POST'])

#app.add_url_rule('/api/used/<option>/<id>', view_func=h_t_f.adding_used_unused, methods=['GET','POST'])

app.add_url_rule('/contact_us', view_func=c_u.contact_us, methods=['GET','POST'])
app.add_url_rule('/signup', view_func=auth.signup, methods=['GET','POST'])
app.add_url_rule('/logout', view_func=auth.logout, methods=['GET','POST'])

app.add_url_rule('/', view_func=auth.login, methods=['GET','POST'])

app.errorhandler(404)(e_p.page_not_found)
app.errorhandler(403)(e_p.forbidden)
app.errorhandler(401)(e_p.unauthorized)
app.errorhandler(500)(e_p.internal_error)

@app.route('/email_sent')
def email_sent():
    return render_template('OnSuccess/EmailSent.html')

@app.route('/journalist_subscribed')
def journalist_subscribed():
    return render_template('OnSuccess/Subscribed.html')
#@app.route('/')
# def welcome():
#     return render_template('welcome.html')



@app.route('/home')
@login_required
def home():
    mp.people_set_once(session['email'], {'$email': session['email'], '$name': session['name'], '$created': datetime.now().isoformat()})
    mp.people_set(session['email'], properties={'$ip': request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)}, meta={'$ip': request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)})
    return render_template('homePage.html')
    #return render_template('welcome_old.html')


if __name__ == '__main__':
    if Config.ENVIRONMENT == 'local':
        app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
    elif Config.ENVIRONMENT == 'server':
        app.run(port=8000, debug=False, threaded=True)


