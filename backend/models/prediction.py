from models import db
from datetime import datetime

class Prediction(db.Model):
    __tablename__ = 'predictions'

    id                = db.Column(db.Integer, primary_key=True)
    student_id        = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=True)
    student_name      = db.Column(db.String(100))
    study_hours       = db.Column(db.Float, nullable=False)
    attendance        = db.Column(db.Float, nullable=False)
    sleep_hours       = db.Column(db.Float, nullable=False)
    previous_score    = db.Column(db.Float, nullable=False)
    extra_curricular  = db.Column(db.Boolean, default=False)
    model_used        = db.Column(db.String(30), nullable=False, default='random_forest')
    predicted_score   = db.Column(db.Float, nullable=False)
    performance_grade = db.Column(db.String(2))
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':               self.id,
            'student_name':     self.student_name,
            'study_hours':      self.study_hours,
            'attendance':       self.attendance,
            'sleep_hours':      self.sleep_hours,
            'previous_score':   self.previous_score,
            'extra_curricular': self.extra_curricular,
            'model_used':       self.model_used,
            'predicted_score':  round(self.predicted_score, 2),
            'performance_grade': self.performance_grade,
            'created_at':       self.created_at.isoformat()
        }
