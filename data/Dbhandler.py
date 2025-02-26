from .Connection import db

class User(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    badges = db.Column(db.String(500), default="")

    def __repr__(self):
        return f"<User {self.id} - {self.name}, Level: {self.level}, XP: {self.xp}>"

class Reward(db.Model):
    __tablename__ = "reward"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    xp_cost = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Reward {self.id} - {self.name}, XP Cost: {self.xp_cost}>"

def format_user(user):
    """Format a user object into a dictionary."""
    return {
        "id": user.id,
        "name": user.name,
        "xp": user.xp,
        "level": user.level,
        "badges": user.badges.split(",") if user.badges else []
    }
