from django.core.mail import send_mail
from django.conf import settings



def send_mailer(message, recipient):
    subject = "OTP Verification"
    message = message
    from_email = "moosaabdullahi45@gmail.com"
    recipient_list = [recipient]
    r = send_mail(subject, message, from_email, recipient_list)
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
            <p>Welcome to moosa. Use the following OTP to complete your Sign Up procedures</p>
            <ul>
                <li>USERNAME: {username}</li>
                <li>PASSWORD: <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2></li>
            </ul>
            <p style="font-size:0.9em;">Regards,<br />moosa</p>
            <hr style="border:none;border-top:1px solid #eee" />
            <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
              <p>Powered by xchangebox</p>
              <p>Shehu shagari way, maitama</p>
              <p>Abuja</p>
            </div>
          </div>
        </div>
    """
    return html