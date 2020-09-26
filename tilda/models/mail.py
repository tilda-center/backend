from email.mime.text import MIMEText


class Mail():
    def __init__(self, to, fromAddr, subject, message, cc=None, bcc=None):
        self.to = to
        self.fromAddr = fromAddr
        self.message = message
        self.subject = subject
        self.cc = cc
        self.bcc = bcc

    @property
    def email(self):
        msg = MIMEText(self.message, 'plain', 'utf-8')
        msg['From'] = self.fromAddr
        msg['Subject'] = self.subject
        msg['To'] = self.to
        return msg
