from flask import render_template

def page_not_found(e):
    return render_template('error_pages/404.html'), 404

def forbidden(e):
    return render_template('error_pages/403.html'), 403

def unauthorized(e):
    return render_template('error_pages/401.html'), 401