from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, IntegerField

from wtforms import validators

class CustomerForm(Form):
    cust_id = HiddenField()
    cust_name = StringField("Cust name",
                    [validators.DataRequired("input cust name"),
                     validators.Length(3, 200, "Cust name must be from 3 to 200 symbols")])

    cust_address = StringField("Cust address",
                            [validators.DataRequired("input cust address"),
                             validators.Length(3, 200, "Cust address must be from 3 to 200 symbols")])

    cust_city = StringField("Cust city",
                               [validators.DataRequired("input cust city"),
                                validators.Length(3, 200, "Cust city must be from 3 to 200 symbols")])

    cust_state = StringField("Cust state",
                               [validators.DataRequired("input cust state"),
                                validators.Length(2, 2, "Cust state must be 2 symbols")])

    cust_zip = IntegerField("Cust zip",
                            [validators.DataRequired("input cust zip"),
                             validators.NumberRange(10000, 999999, "Cust zip must be correct")])

    cust_country = StringField("Cust country",
                             [validators.DataRequired("input cust country"),
                              validators.Length(3, 200,  "Cust country must be from 3 to 200 symbols")])

    cust_contact = StringField("Cust contact",
                             [validators.DataRequired("input cust contact"),
                              validators.Length(2, 100, "Cust contact must be from 2 to 100 symbols")])

    cust_email = StringField("Cust email",
                             [validators.Length(5, 100, "Cust email must be from 5 to 100 symbols")])

    submit = SubmitField("Save")