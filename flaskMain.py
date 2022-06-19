from flask import render_template
from flask_app.scripts.create_flask_app import app
from flask_app.scripts.EmailVerification import ev_flask_functions as ev_f_f
from flask_app.scripts.JournalistSubscription import journalist_upload_functions as j_u_f
from flask_app.scripts.HaroTable import haro_table_functions as h_t_f
from flask_app.scripts.LoginSignUp import auth
from flask_app.scripts import error_pages as e_p


app.add_url_rule('/email_verification', view_func=ev_f_f.email_verification, methods=['GET','POST'])
app.add_url_rule('/journalists', view_func=j_u_f.load_journalist_file, methods=['GET','POST'])

app.add_url_rule('/haros', view_func=h_t_f.show_haro_table, methods=['GET'])
app.add_url_rule('/api/serveHaros', view_func=h_t_f.serve_data, methods=['GET','POST'])
app.add_url_rule('/api/serveHaros/<option>', view_func=h_t_f.serve_data, methods=['GET','POST'])
app.add_url_rule('/api/used/<option>/<id>', view_func=h_t_f.adding_used_unused, methods=['GET','POST'])

app.add_url_rule('/login', view_func=auth.login, methods=['GET','POST'])
app.add_url_rule('/signup', view_func=auth.signup, methods=['GET','POST'])
app.add_url_rule('/logout', view_func=auth.logout, methods=['GET','POST'])

app.errorhandler(404)(e_p.page_not_found)
app.errorhandler(403)(e_p.forbidden)
app.errorhandler(401)(e_p.unauthorized)



@app.route('/')
def welcome():
    return render_template('welcome.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
    # app.run(port=8000, debug=False, threaded=True) on server

