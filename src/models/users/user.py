import uuid

from src.common.Utils import Utils
from src.common.database import Database
import src.models.users.errors as UserErrors
from src.models.alerts.alert import Alert
import src.models.users.constants as UserConstants

__author__ = 'ishween'


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies an e-mail/password combo is valid or not.
        Checks that the e-mail exists, and that the password associated to that e-mail is correct.
        :param email: The users's e-mail
        :param password: A sha512 hashed password
        :return: true if valid, false otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email":email}) # password in shah512 -> sha512_pbkdf2
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your users data not exist")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password is wrong")
        return True

    @staticmethod
    def register_user(email, password):
        """
        This method registers users using email and password.
        password comes encrypt as sha512
        :param email: users's email
        :param password: password as sha512
        :return: true id registered, false otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION,{"email":email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("You are already Registered")
        if not Utils.email_is_valid(email):
            raise  UserErrors.InvalidEmailError("Invalid e-mail id")
        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert("users", self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email':email}))

    def get_user_alert(self):
        return Alert.find_by_email(self.email)


