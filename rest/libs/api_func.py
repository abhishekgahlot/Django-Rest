import AESCipher
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime

SECRET_KEY = '$4745cdb35ab5812151b00f8a6ba3d75'

def api_token(username):
    c = AESCipher.Cipher(SECRET_KEY)
    token = c.encrypt(username + '|' + str(datetime.datetime.now()) + '|')
    return token

def verify_token(token,username):
    c = AESCipher.Cipher(SECRET_KEY)
    try:
        token = c.decrypt(token)
        if username == token.split('|')[0]:
            return True
        else:
            return False
    except:
        return False

def check_email(email):
    try:
        validate_email(email)
    except ValidationError:
        return False
    else:
        return True