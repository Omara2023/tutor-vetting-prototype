import os
from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from engine import OpenRouterClient
from models import db, Tutor, Priority

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
client = OpenRouterClient()

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    tutors = Tutor.query.order_by(Tutor.score.desc()).all()
    priorities = Priority.query.all()
    return render_template("index.html", tutors=tutors, priorities=priorities)

@app.route("/seed")
def seed():
    """Run this once to populate your demo data"""
    if not Tutor.query.first():
        t1 = Tutor(name="Alice Smith", subject="Maths", cv_text="GCSE Maths specialist. 5 years experience. DBS 2027.")
        t2 = Tutor(name="Bob Jones", subject="Physics", cv_text="University lecturer. 10 years experience. DBS 2023 (EXPIRED).")
        db.session.add_all([t1, t2])
        db.session.add(Priority(category="Maths", weight=9))
        db.session.commit()
    return "Database Seeded!"

@app.route("/vet/<int:tutor_id>", methods=["POST"])
def vet_tutor(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)
    prompt = f"Analyse this tutor: {tutor.cv_text}. Check if DBS is expired (Current Year 2026). Provide a 1-sentence verdict."
    analysis = client.generate(prompt)

    return jsonify({"analysis": analysis})

@app.route("/rank_all", methods=["POST"])
def rank_candidates():
    priorities = Priority.query.all()
    priority_string = ", ".join([f"{p.category} (weight {p.weight})" for p in priorities])
    
    tutors = Tutor.query.all()
    for tutor in tutors:
        prompt = f"Given these hiring priorities: {priority_string}, rate this tutor's CV out of 100: {tutor.cv_text}. Return ONLY the number."
        try:
            score_text = client.generate(prompt).strip()
            tutor.score = float("".join(filter(str.isdigit, score_text)) or 0)
        except Exception as e:
            print(f"Error ranking {tutor.name}: {e}")
    
    db.session.commit()
    return jsonify({"status": "Success"})

@app.route("/priorities", methods=["GET", "POST"])
def manage_priorities():
    if request.method == "POST":
        category = request.form.get("category")
        weight = int(request.form.get("weight", 5))
        
        priority = Priority.query.filter_by(category=category).first()
        if priority:
            priority.weight = weight
        else:
            new_p = Priority(category=category, weight=weight)
            db.session.add(new_p)
        
        db.session.commit()
        return redirect("/priorities")
    
    priorities = Priority.query.all()
    return render_template("priorities.html", priorities=priorities)

@app.route("/priorities/delete/<int:id>")
def delete_priority(id):
    p = Priority.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect("/priorities")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

def expand_priorities(priorities_list: list):
    """priorities_list: [{'category': 'Maths', 'weight': 8}, ...]"""
    prompt = f"Convert these hiring priorities into a list of 5 key technical keywords for a semantic search: {priorities_list}"
    keywords = client.generate(prompt)
    return keywords