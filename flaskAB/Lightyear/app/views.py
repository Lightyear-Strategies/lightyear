from flask import render_template, flash
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi, expose, BaseView, has_access, SimpleFormView
from wtforms import Form, StringField
from wtforms.validators import DataRequired
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_babel import lazy_gettext as _

from . import appbuilder, db


class MyFormView(SimpleFormView):
    form = MyForm
    form_title = "This is my first form view"
    message = "My form was submitted"

    def form_get(self, form):
        form.field1.data = "This was prefilled"

    def form_post(self, form):
        # post process form
        flash(self.message, "info")


appbuilder.add_view(
    MyFormView,
    "My form View",
    icon="fa-group",
    label=_("My form View"),
    category="My Forms",
    category_icon="fa-cogs",
)


"""
    Application wide 404 error handler
"""

@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()
