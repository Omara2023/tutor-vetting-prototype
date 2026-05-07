import csv
from models import db, Tutor, Document, Priority

class Seeder:
    def __init__(self, file_path='candidates.csv') -> None:
        self.file_path = file_path

    def seed(self):
        """Harvests candidates from CSV and populates Document relationships"""
        
        # 1. Clear existing data for a clean demo
        db.drop_all()
        db.create_all()

        # 2. Add default Priorities (Business Logic)
        default_priorities = [
            Priority(category="Maths", weight=9),
            Priority(category="Physics", weight=7),
            Priority(category="English", weight=5)
        ]
        db.session.add_all(default_priorities)

        # 3. Read and Create Tutors + Documents
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Create the sub-documents
                    cv_doc = Document(type='CV', content=row['cv_content'])
                    dbs_doc = Document(type='DBS', content=row['dbs_content'])
                    lesson_doc = Document(type='LESSON', content=row['lesson_content'])
                    
                    db.session.add_all([cv_doc, dbs_doc, lesson_doc])
                    db.session.commit() # Commit to get IDs

                    # Create the Tutor linked to those IDs
                    tutor = Tutor(
                        name=row['name'],
                        subject=row['subject'],
                        score=0.0,
                        cv_id=cv_doc.id,
                        dbs_id=dbs_doc.id,
                        lesson_id=lesson_doc.id
                    )
                    db.session.add(tutor)
                
                db.session.commit()
            return f"Success: 10 Candidates harvested from {self.file_path}!"
        
        except Exception as e:
            db.session.rollback()
            return f"Error seeding data: {str(e)}"