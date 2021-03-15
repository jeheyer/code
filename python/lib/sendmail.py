from smtplib import SMTP

class Email():

    def __init__(self, recipient, sender = None, subject = None, body = None):

        if not sender:
            self.sender = "nobody@localhost"
        else:
            self.sender = sender

        self.recipient = recipient
        header = "From: <" + self.sender + ">\n"
        header += "To: <" + self.recipient + ">\n"
        if subject:
            self.subject = subject
        else:
            self.subject = ""
        header += "Subject: " + self.subject + "\n\n"
        if body:
            self.body = body
        else:
            self.body = ""
        contents = header + self.body

        try:
            smtpObj = SMTP('localhost')
            smtpObj.sendmail(self.sender, self.recipient, contents)
        except:
            raise Exception("Error: unable to send email")

