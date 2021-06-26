from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, IntegerField

from wtforms import validators

class VendorForm(Form):
    vend_id = HiddenField()
    vend_name = StringField("Vend name",
                    [validators.DataRequired("input vend name"),
                     validators.Length(3, 200, "vend name must be from 3 to 200 symbols")])

    vend_address = StringField("Vend address",
                            [validators.DataRequired("input vend address"),
                             validators.Length(3, 200, "Vend address must be from 3 to 200 symbols")])

    vend_city = StringField("Vend city",
                               [validators.DataRequired("input vend city"),
                                validators.Length(3, 200, "Vend city must be from 3 to 200 symbols")])

    vend_state = StringField("Vend state",
                               [validators.DataRequired("input vend state"),
                                validators.Length(2, 2, "Vend state must be 2 symbols")])

    vend_zip = IntegerField("Vend zip",
                            [validators.DataRequired("input vend zip"),
                             validators.NumberRange(10000, 999999, "Vend zip must be correct")])

    vend_country = StringField("Vend country",
                             [validators.DataRequired("input vend country"),
                              validators.Length(3, 200,  "Vend country must be from 3 to 200 symbols")])


    submit = SubmitField("Save")