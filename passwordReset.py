from .__init__ import db
from .models import User
import os

class ResetManager():
    def __init__(self):
        self.db = db

    def sendEmailForReset(email: str) -> bool:
        user = User.query.filter_by(email=email).first()

        # Check if user does not exist
        if not user:
            return False

        resetURL = "http://13.57.204.89/reset?email=" + email
        os.system('echo "Please reset your email at:' + resetURL + '" | mail -s "Team 8 Bank Of Trojans Password Reset" ' + email)
        return True

    def resetPasswordForEmail(email: str, newPassword: str) -> bool:
        user = User.query.filter_by(email=email).first()

        # Check if user does not exist
        if not user:
            return False

        try:
            user.password = newPassword
            db.session.commit()
        except:
            return False

        return True
