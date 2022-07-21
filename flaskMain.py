from flask import render_template
from flask_app.scripts.create_flask_app import app
from flask_app.scripts.EmailValidator import ev_flask_functions as ev_f_f
from flask_app.scripts.PeriodicWriters import journalist_upload_functions as j_u_f
from flask_app.scripts.HaroTable import haro_table_functions as h_t_f
from flask_app.scripts.ContactUs import contact_us as c_u
from flask_app.scripts.LoginSignUp import auth
from flask_app.scripts import error_pages as e_p
from flask_app.scripts.config import Config


app.add_url_rule('/email_validator', view_func=ev_f_f.email_validator, methods=['GET','POST'])
app.add_url_rule('/writers', view_func=j_u_f.load_journalist_file, methods=['GET','POST'])
app.add_url_rule('/unsubscribe/<token>', view_func=j_u_f.unsubscribe, methods=['GET','POST'], endpoint='unsubscribe')

app.add_url_rule('/haro_table', view_func=h_t_f.show_haro_table, methods=['GET'])
app.add_url_rule('/api/serveHaros', view_func=h_t_f.serve_data, methods=['GET','POST'])
app.add_url_rule('/api/serveHaros/<option>', view_func=h_t_f.serve_data, methods=['GET','POST'])
app.add_url_rule('/api/used/<option>/<id>', view_func=h_t_f.adding_used_unused, methods=['GET','POST'])

app.add_url_rule('/contact_us', view_func=c_u.contact_us, methods=['GET','POST'])
app.add_url_rule('/', view_func=auth.login, methods=['GET','POST'])
app.add_url_rule('/signup', view_func=auth.signup, methods=['GET','POST'])
app.add_url_rule('/logout', view_func=auth.logout, methods=['GET','POST'])

app.errorhandler(404)(e_p.page_not_found)
app.errorhandler(403)(e_p.forbidden)
app.errorhandler(401)(e_p.unauthorized)
app.errorhandler(500)(e_p.internal_error)


@app.route('/')
# def welcome():
#     return render_template('welcome.html')


@app.route('/home')
def home():
    #return render_template('homePage.html')
    return render_template('welcome_old.html')


if __name__ == '__main__':
    if Config.ENVIRONMENT == 'local':
        app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
    elif Config.ENVIRONMENT == 'server':
        app.run(port=8000, debug=False, threaded=True)


