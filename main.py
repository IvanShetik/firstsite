from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms.customer_form import CustomerForm
from forms.vendor_form import  VendorForm
from sqlalchemy.sql import func

app = Flask(__name__)

db = SQLAlchemy(app)

app.secret_key = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Qwerty0901@localhost/postgres"

class Customers(db.Model):
    __tablename__ = "customers"
    cust_id = db.Column(db.CHAR(10), primary_key = True)
    cust_name = db.Column(db.CHAR(50), nullable = False)
    cust_address = db.Column(db.CHAR(50), nullable = True)
    cust_city = db.Column(db.CHAR(50), nullable = True)
    cust_state = db.Column(db.CHAR(5), nullable = True)
    cust_state = db.Column(db.CHAR(5), nullable=True)
    cust_zip = db.Column(db.CHAR(10), nullable=True)
    cust_country = db.Column(db.CHAR(50), nullable=True)
    cust_contact = db.Column(db.CHAR(50), nullable=True)
    cust_email = db.Column(db.CHAR(255), nullable=True)

    orders = db.relationship("Orders")


class Orders(db.Model):
    __tablename__ = "orders"
    cust_id = db.Column(db.CHAR(10), db.ForeignKey("customers.cust_id"))
    order_num = db.Column(db.Integer(), primary_key = True)
    order_date = db.Column(db.Date(), nullable=False)

    orderitems = db.relationship("Orderitems")


class Orderitems(db.Model):
    __tablename__ = "orderitems"
    order_num = db.Column(db.Integer(), db.ForeignKey("orders.order_num"))
    order_item = db.Column(db.Integer(), primary_key=True)
    prod_id = db.Column(db.CHAR(10), db.ForeignKey("products.prod_id") )
    quantity = db.Column(db.Integer(), nullable = False)
    item_price = db.Column(db.Numeric(8), nullable=False)



class Products(db.Model):
    __tablename__ = "products"
    prod_id = db.Column(db.CHAR(10), primary_key = True)
    vend_id = db.Column(db.CHAR(10), db.ForeignKey("vendors.vend_id"))
    prod_name = db.Column(db.CHAR(255), nullable=False)
    prod_price = db.Column(db.Numeric(8), nullable = False)
    prod_desc = db.Column(db.String(1000), nullable = True)

    orderitems = db.relationship("Orderitems")


class Vendors(db.Model):
    __tablename__ = "vendors"
    vend_id = db.Column(db.CHAR(10), primary_key=True)
    vend_name = db.Column(db.CHAR(50), nullable = False)
    vend_address = db.Column(db.CHAR(50), nullable = True)
    vend_city = db.Column(db.CHAR(50), nullable=True)
    vend_state = db.Column(db.CHAR(5), nullable=True)
    vend_zip = db.Column(db.CHAR(10), nullable=True)
    vend_country = db.Column(db.CHAR(50), nullable=True)

    products = db.relationship("Products")


@app.route("/")
def start():
    return render_template("index.html")

#customers

@app.route("/edit_customer", methods = ['GET', 'POST'])
def edit_customer():
    form = CustomerForm()
    if request.method == "GET":
        customer_id  = request.args.get("cust_id")
        customer = db.session.query(Customers).filter(Customers.cust_id == customer_id).one()

        form.cust_id.data = customer_id.strip()
        form.cust_name.data = customer.cust_name.strip()
        form.cust_address.data = customer.cust_address.strip()
        form.cust_city.data = customer.cust_city.strip()
        form.cust_state.data = customer.cust_state.strip()
        form.cust_zip.data = customer.cust_zip.strip()
        form.cust_country.data = customer.cust_country.strip()
        form.cust_contact.data = customer.cust_contact.strip()
        form.cust_email.data = customer.cust_email.strip()

        return render_template("customer_form.html", form = form, form_name = "Edit customer", action = "/edit_customer")
    else:
        if not form.validate():
            return render_template("customer_form.html", form=form, form_name="Edit customer", action="/edit_customer")
        else:
            customer = db.session.query(Customers).filter(Customers.cust_id == form.cust_id.data).one()

            customer.cust_name = form.cust_name.data
            customer.cust_address = form.cust_address.data
            customer.cust_city = form.cust_city.data
            customer.cust_state = form.cust_state.data
            customer.cust_zip = form.cust_zip.data
            customer.cust_country = form.cust_country.data
            customer.cust_contact = form.cust_contact.data
            customer.cust_email = form.cust_email.data
            db.session.commit()

            return redirect(url_for("customers"))


@app.route("/delete_customer", methods = ["POST"])
def delete_customer():
    customer_id = request.form["cust_id"]

    orderitems = db.session.query(Orderitems).join(Products, Products.prod_id == Orderitems.prod_id).join(Vendors, Vendors.vend_id == Products.vend_id).filter()

    result = db.session.query(Customers).filter(Customers.cust_id == customer_id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for("customers"))

@app.route("/new_customer", methods = ["GET", "POST"])
def new_customer():
    form = CustomerForm()
    if request.method == "POST":
        if not form.validate():
            return render_template("customer_form.html", form=form, form_name="New customer", action="/new_customer")
        else:
            max_id = int(db.session.query(func.max(Customers.cust_id)).one()[0])
            new_customer = Customers(
                cust_id = max_id + 1,
                cust_name = form.cust_name.data,
                cust_address = form.cust_address.data,
                cust_city = form.cust_city.data,
                cust_state = form.cust_state.data,
                cust_zip = form.cust_zip.data,
                cust_country = form.cust_country.data,
                cust_contact = form.cust_contact.data,
                cust_email = form.cust_email.data,
            )
            db.session.add(new_customer)
            db.session.commit()

            return redirect(url_for("customers"))
    return render_template("customer_form.html", form=form, form_name="New customer", action="/new_customer")

@app.route("/customers")
def customers():
    customers = db.session.query(Customers).all()
    return render_template("customer.html", customers = customers)

#vendors
@app.route("/edit_vendor", methods = ['GET', 'POST'])
def edit_vendor():
    form = VendorForm()
    if request.method == "GET":
        vend_id  = request.args.get("vend_id")
        vendor = db.session.query(Vendors).filter(Vendors.vend_id == vend_id).one()

        form.vend_id.data = vend_id.strip()
        form.vend_name.data = vendor.vend_name.strip()
        form.vend_address.data = vendor.vend_address.strip()
        form.vend_city.data = vendor.vend_city.strip()
        form.vend_state.data = "" if vendor.vend_state is None else vendor.vend_state.strip()
        form.vend_zip.data = vendor.vend_zip.strip()
        form.vend_country.data = vendor.vend_country.strip()


        return render_template("vendor_form.html", form = form, form_name = "Edit vendor", action = "/edit_vendor")
    else:
        if not form.validate():
            return render_template("vendor_form.html", form=form, form_name="Edit vendor", action="/edit_vendor")
        else:
            vendor = db.session.query(Vendors).filter(Vendors.vend_id == form.vend_id.data).one()

            vendor.vend_name = form.vend_name.data
            vendor.vend_address = form.vend_address.data
            vendor.vend_city = form.vend_city.data
            vendor.vend_state = form.vend_state.data
            vendor.vend_zip = form.vend_zip.data
            vendor.vend_country = form.vend_country.data
            db.session.commit()

            return redirect(url_for("vendors"))

@app.route("/delete_vendor", methods = ["POST"])
def delete_vendor():
    vendor_id = request.form["vend_id"]

    orderitems = db.session.query(Orderitems).\
        join(Products, Products.prod_id == Orderitems.prod_id).\
        join(Vendors, Vendors.vend_id == Products.vend_id).\
        filter(Vendors.vend_id == vendor_id).all()
    for i in orderitems:
        db.session.delete(i)
        print(i.order_num)

    products = db.session.query(Products). \
        join(Vendors, Vendors.vend_id == Products.vend_id). \
        filter(Vendors.vend_id == vendor_id).all()
    for i in products:
        db.session.delete(i)

    result = db.session.query(Vendors).filter(Vendors.vend_id == vendor_id).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for("vendors"))


@app.route("/new_vendor", methods = ["GET", "POST"])
def new_vendor():
    form = VendorForm()
    if request.method == "POST":
        if not form.validate():
            return render_template("vendor_form.html", form=form, form_name="New vendor", action="/new_vendor")
        else:
            ids = db.session.query(func.max(Vendors.vend_id)).one()[0]
            string = ""
            num = ""
            for word in ids:
                if word.isdigit() == False:
                    string+=word
                else:
                    num += word

            new_vendor = Vendors(
                vend_id = string.strip()+str(int(num)+1),
                vend_name = form.vend_name.data,
                vend_address = form.vend_address.data,
                vend_city = form.vend_city.data,
                vend_state = form.vend_state.data,
                vend_zip = form.vend_zip.data,
                vend_country = form.vend_country.data,

            )
            db.session.add(new_vendor)
            db.session.commit()

            return redirect(url_for("vendors"))
    return render_template("vendor_form.html", form=form, form_name="New vendor", action="/new_vendor")

@app.route("/vendors")
def vendors():
    vendors = db.session.query(Vendors).all()
    return render_template("vendor.html", vendors = vendors)


if __name__ == "__main__":
    app.run()