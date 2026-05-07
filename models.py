from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subject = db.Column(db.String(50))
    score = db.Column(db.Float, default=0.0)
    justification = db.Column(db.Text) # For the "Why 87?" blurb
    
    #Relationships
    cv_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    dbs_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('document.id'))

    cv = db.relationship('Document', foreign_keys=[cv_id])
    dbs = db.relationship('Document', foreign_keys=[dbs_id])
    lesson = db.relationship('Document', foreign_keys=[lesson_id])

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20)) # 'CV', 'DBS', 'LESSON'
    content = db.Column(db.Text)    # Synthetic text content

class Priority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50)) # e.g., 'Maths', 'Experience'
    weight = db.Column(db.Integer, default=5) # 1-10 scale