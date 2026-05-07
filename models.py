from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subject = db.Column(db.String(50))
    cv_text = db.Column(db.Text)
    dbs_status = db.Column(db.String(20), default="Pending")
    score = db.Column(db.Float, default=0.0)

class Priority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50)) # e.g., 'Maths', 'Experience'
    weight = db.Column(db.Integer, default=5) # 1-10 scale