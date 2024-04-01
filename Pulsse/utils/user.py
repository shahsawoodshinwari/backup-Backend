from passlib.hash import pbkdf2_sha256

from Pulsse.models.user import User


def email_in_db(email, password):

    user = User.query.filter_by(email=email.lower()).first()
    if user is None:
        return False
    else:
        return True

from passlib.hash import pbkdf2_sha256

def email_password_in_db(email, password):
    user = User.query.filter_by(email=email.lower()).first()

    if user is None:
        return False
    else:
        # Verify the hashed password
        if pbkdf2_sha256.verify(password, user.password):
            return True
        else:
            return False


def forget_password_email(email):

    for product in User.objects(email=email.lower()):
        if product:
            return True
        else:
            return False


def same_email(email, mycol):
    email_list = []
    for x in mycol.find():
        email_list.append(x['email'])
    if email in email_list:
        return email
    else:
        return False


def new_password_check(password):

    if len(password) < 6 or password.isspace():
        return False

    else:
        return True


def true_false_check(check):
    check = check.strip()

    if check.lower() == 'true':
        return True

    elif check.lower() == 'false':

        return False

    else:
        return 0

def email_in_check_db(email):
    # Check if the provided email is already registered for a different user
    print("Email in func ", email)
    user = User.query.filter_by(email=email.lower()).first()
    if user is None:
        print("False")
        return False
    else:
        print("True")
        return True