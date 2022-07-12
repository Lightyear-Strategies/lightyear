from flask import render_template

def page_not_found(e):
    return render_template('ErrorPages/404.html'), 404

def forbidden(e):
    return render_template('ErrorPages/403.html'), 403

def unauthorized(e):
    return render_template('ErrorPages/401.html'), 401

def internal_error(e):
    return render_template('ErrorPages/500.html'), 500