import random
import string
import hashlib
import binascii
import smtplib
import random
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings




# def generate_random_code():
#     return 'school_name'.join(random.choice(string.ascii_lowercase + string.digits, k=4))
RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
# def generate_user_id(length,account_type, allowed_chars="1234567890"):
#     result = None
#     if account_type == "teacher":
#         result = "tch"
#     if account_type == "student":
#         result = "stud"
#     if account_type == "parent":
#         result = "prt"
    
#     return (f"{result}{get_random_string(length, allowed_chars)}")

def generate_random_number():
    return str(random.randint(1000, 9999))


def generate_username(role, code):
    roles_dict = {'Teacher':'tch', 'Student':'std', 'Parent':'prt'}
    return roles_dict[role] + str(code)
    # code = SchoolUser.objects.latest().id +1
    # title = None
    # if role == 'Student':
    #     title =  'stud' + generate_random_number()
    # elif role == 'Parent':
    #     title =  'par' + generate_random_number()
    # elif role == 'Teacher':
    #     title =  'tch' + generate_random_number()
    # return title 

def hash_password(ppt):
    bppt = ppt.encode()
    pct = hashlib.pbkdf2_hmac("sha256", bppt, b"m@ssa", 10000)
    dehex = binascii.hexlify(pct)
    hash_pass = dehex.decode()
    return hash_pass


def send_mailer(**kwargs):
    subject = "OTP Verification"
    message = kwargs["message"]
    from_email = "moosaabdullahi45@gmail.com"
    recipient_list = [kwargs["recipient"]]
    # msg_html = render_to_string('templates/email.html', {'some_params': some_params})
    html_message = f"""
        <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
          <div style="margin:50px auto;width:70%;padding:20px 0">
            <div style="border-bottom:1px solid #eee">
              <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600"></a>
            </div>
            <p style="font-size:1.1em">Hi,</p>
            <p>Welcome to SMS. Use the following OTP to complete your Sign Up procedures</p>
            <ul>
                <li>USERNAME: {kwargs["username"]}</li>
                <li>PASSWORD: <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{kwargs["otp"]}</h2></li>
            </ul>
            <p style="font-size:0.9em;">Regards,<br />moosa</p>
            <hr style="border:none;border-top:1px solid #eee" />
          </div>
        </div>
    """
    r = send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    print("RRRRRRRRRR")
    print(r)
    return r 

def get_otp_html_message(otp, username=None):
    html = f"""
        <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
          <div style="margin:50px auto;width:70%;padding:20px 0">
            <div style="border-bottom:1px solid #eee">
              <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600"></a>
            </div>
            <p style="font-size:1.1em">Hi,</p>
            <p>Welcome to SMS. Use the following OTP to complete your Sign Up procedures</p>
            <ul>
                <li>USERNAME: {username}</li>
                <li>PASSWORD: <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2></li>
            </ul>
            <p style="font-size:0.9em;">Regards,<br />moosa</p>
            <hr style="border:none;border-top:1px solid #eee" />
          </div>
        </div>
    """
    return html