# Import smtplib for the actual sending function
import smtplib

from getpass import getpass
# Import the email modules we'll need
from email.mime.text import MIMEText



SMTP_ADDR = ''
SMTP_PORT = 25
SMTP_USER = ''
DEFAULT_SUBJECT = 'REVISIONS'

def send_mail(msg=None, user_login_creds=None, sender=None, recipients=None):
  
    try:
        smtpserver = smtplib.SMTP(SMTP_ADDR, SMTP_PORT)
        smtpserver.set_debuglevel(False)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo        
        # getpass() prompts the user for their password (so it never appears in plain text)
        # smtpserver.login(SMTP_USER, getpass('Password for user %s: ' % SMTP_USER))
        smtpserver.login(*user_login_creds())
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        smtpserver.sendmail(sender, recipients, msg.as_string())
        print "Message sent to '%s'." % recipients 
        smtpserver.quit()
    except smtplib.SMTPAuthenticationError as e:
        print "Unable to send message: %s" % e
    return True

def create_mime_msg(msg=None, subject=None, sender=None, recipients=None):
    msg            = MIMEText(msg, 'html')
    msg['Subject'] = subject
    msg['From']    = sender
    msg['To']      = ', '.join(recipients)
    return msg


