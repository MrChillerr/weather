from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Results(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    location = db.Column(db.Text(), nullable=False)
    feels_like = db.Column(db.Text(), nullable=False)
    temp = db.Column(db.Text(), nullable=False)
    dt_obj = db.Column(db.Text(), nullable=False)
    icon_url = db.Column(db.Text(), nullable=False)
    weather = db.Column(db.Text(), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'location': self.location,
            'feels_like': self.feels_like,
            'temp': self.temp,
            'dt_obj': self.dt_obj,
            'icon_url': self.icon_url,
            'weather': self.weather,
        }