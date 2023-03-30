from datetime import datetime

from core import db


class Pic(db.Model):

    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(225), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    updated_at = db.Column(
        db.DateTime(), default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )


    def __str__(self) -> str:
        return f"{self.name} - {self.latitude} - {self.longitude} "

    def __repr__(self):
        return f"Pic({self.id}, {self.name})"

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def remove(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude
        }
