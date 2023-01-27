import random
import string
import hashlib
import binascii
import smtplib
import random
from django.utils.crypto import get_random_string
from .models import *


def generate_username(role):
    user_code = {
        'Student':('std',),
        'Parent':('prt',),
        'Teacher':('tch', TeacherAccount.objects.latest('id')+1)}
    return user_code[role][0] + '/' + user_code[role][1]


def hash_password(ppt):
    bppt = ppt.encode()
    pct = hashlib.pbkdf2_hmac("sha256", bppt, b"m@ssa", 10000)
    dehex = binascii.hexlify(pct)
    hash_pass = dehex.decode()
    return hash_pass