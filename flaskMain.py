from flask import render_template
from flask_app.scripts.create_flask_app import app
from flask_app.scripts.EmailVerification import ev_flask_functions as ev_f_f
from flask_app.scripts.JournalistSubscription import journalist_upload_functions as j_u_f
from flask_app.scripts.HaroTable import haro_table_functions as h_t_f
from flask_app.scripts.LoginRegister import auth

app.add_url_rule('/email_verification', view_func=ev_f_f.email_verification, methods=['GET','POST'])
app.add_url_rule('/journalists', view_func=j_u_f.load_journalist_file, methods=['GET','POST'])

app.add_url_rule('/haros', view_func=h_t_f.show_haro_table, methods=['GET'])
app.add_url_rule('/api/serveHaros', view_func=h_t_f.serve_data, methods=['GET','POST'])
app.add_url_rule('/api/serveHaros/<option>', view_func=h_t_f.serve_data, methods=['GET','POST'])
app.add_url_rule('/api/used/<option>/<id>', view_func=h_t_f.adding_used_unused, methods=['GET','POST'])

app.add_url_rule('/login', view_func=auth.login, methods=['GET','POST'])
app.add_url_rule('/register', view_func=auth.register, methods=['GET','POST'])
app.add_url_rule('/logout', view_func=auth.logout, methods=['GET','POST'])


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)


