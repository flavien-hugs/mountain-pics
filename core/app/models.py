from datetime import datetime

from app import db


class Peak(db.Model):

    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(225), nullable=False)
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
        return f"Peak({self.id}, {self.name})"

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def remove(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    def to_json(self):

        data = {
            "id": self.id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude
        }

        return data
