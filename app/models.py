from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique=True)
    session = db.Column(db.String())

    def update_session(self, new_session):
        self.session = new_session
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.username)

