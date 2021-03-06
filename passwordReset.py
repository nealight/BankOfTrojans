from .__init__ import db
from .models import User
import os
from werkzeug.security import generate_password_hash

class ResetManager():
    def __init__(self):
        self.db = db

    def sendEmailForReset(email: str) -> bool:
        user = User.query.filter_by(email=email).first()

        # Check if user does not exist
        if not user:
            return False

        if user.resetCount:
            user.resetCount += 1
        else:
            user.resetCount = 1
        
        db.session.commit()
        
        resetURL = "http://13.57.204.89/reset?email=" + email
        os.system('echo "Please reset your email at: ' + resetURL + '" | mail -s "Team 8 Bank Of Trojans Password Reset" ' + email)
        return True

    def resetPasswordForEmail(email: str, newPassword: str) -> bool:
        user = User.query.filter_by(email=email).first()

        # Check if user does not exist
        if not user:
            return False

        try:
            user.password = generate_password_hash(newPassword, method='pbkdf2:md5')
            db.session.commit()
        except:
            return False

        return True
