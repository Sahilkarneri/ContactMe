from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = "<YOUR SECRET KEY>"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCMEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# with app.app_context():
#     db.create_all()

ma = Marshmallow(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)

    def __init__(self, firstname, lastname, email, description):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.description = description


# Contact Schema for serilizaing and deseriliazing json objects
class ContactSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstname', 'lastname', 'email', 'description')

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

# @app.route("/", methods=['GET'])
# def get():
#     return jsonify({'msg':'Hello World!'})

# Create add new contact
@app.route('/contact', methods=['POST'])
def create_contact():
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    description = request.json['description']

    new_contact = Contact(firstname, lastname, email, description)

    db.session.add(new_contact)
    db.session.commit()

    return contact_schema.jsonify(new_contact)

# Get All Contacts
@app.route('/contact', methods=['GET'])
def get_contacts():
    all_contacts = Contact.query.all()
    result = contacts_schema.dump(all_contacts)
    return jsonify(result)

# Get contact by id
@app.route('/contact/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id)
    return contact_schema.jsonify(contact)

# Update contact by id
@app.route('/contact/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get(id)

    firstname = request.json['firstname']
    lastname = request.json['lastname']
    email = request.json['email']
    description = request.json['description']

    contact.firstname = firstname
    contact.lastname = lastname
    contact.email = email
    contact.description = description

    db.session.commit()

    return contact_schema.jsonify(contact)

# Delete contact by id
@app.route('/contact/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    
    db.session.delete(contact)
    db.session.commit()

    return contact_schema.jsonify(contact)

# run server
if __name__ == "__main__":
    app.run(debug=True)