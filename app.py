from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///suggestions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.static_folder = 'static'  # Set the static folder for serving CSS and other static files
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(500), nullable=False)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    comment = request.form['comment']
    feedback = Feedback(name=name, comment=comment)
    db.session.add(feedback)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET'])
def admin():
    feedbacks = Feedback.query.all()
    return render_template('admin.html', feedbacks=feedbacks)


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    feedback = Feedback.query.get_or_404(id)
    db.session.delete(feedback)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    feedback = Feedback.query.get_or_404(id)
    if request.method == 'POST':
        feedback.name = request.form['name']
        feedback.comment = request.form['comment']
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit.html', feedback=feedback)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
