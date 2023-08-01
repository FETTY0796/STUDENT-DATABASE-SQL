from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def home():
    students = Student.query.all()
    return render_template('home.html', students=students)
@app.route('/create', methods=['POST'])

def create():
    student_id = request.form.get('student_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    dob = request.form.get('dob')
    if not dob:
        # Return an error message if 'dob' field is empty
        return "Error: Date of birth field is required", 400

    dob = datetime.strptime(dob, "%Y-%m-%d").date()

    amount_due = request.form.get('amount_due')
    
    new_student = Student(
        student_id=student_id,
        first_name=first_name,
        last_name=last_name,
        dob=dob,
        amount_due=amount_due
    )
    db.session.add(new_student)
    db.session.commit()
    
    return redirect('/')


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # creates the tables
    app.run(debug=True)

@app.route('/students', methods=['POST'])


def create_student():
    data = request.get_json()
    dob = datetime.strptime(data['dob'], '%Y-%m-%d')
    new_student = Student(
        student_id=data['student_id'], 
        first_name=data['first_name'],
        last_name=data['last_name'],
        dob=dob,
        amount_due=data['amount_due']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'new student created'})

@app.route('/students/<student_id>', methods=['GET'])


def get_student(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if student:
        return jsonify({
            'student_id': student.student_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'dob': student.dob.isoformat(),
            'amount_due': student.amount_due
        })
    else:
        return jsonify({'message': 'student not found'})

@app.route('/students/<student_id>', methods=['PUT'])


def update_student(student_id):
    data = request.get_json()
    student = Student.query.filter_by(student_id=student_id).first()
    if student:
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.dob = datetime.strptime(data['dob'], '%Y-%m-%d')
        student.amount_due = data['amount_due']
        db.session.commit()
        return jsonify({'message': 'student data updated'})
    else:
        return jsonify({'message': 'student not found'})


@app.route('/students', methods=['GET'])
def get_all_students():
    students = Student.query.all()
    output = []
    for student in students:
        student_data = {
            'student_id': student.student_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'dob': student.dob.isoformat(),
            'amount_due': student.amount_due
        }
        output.append(student_data)
    return jsonify({'students': output})

@app.route('/delete/<student_id>', methods=['POST'])
def delete(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'student deleted'})
    else:
        return jsonify ({'message': 'student not found'}) 

    


if __name__ == '__main__':
    db.create_all() # creates the tables
    app.run(debug=True)
