from smtplib import SMTP


def sendmail(config, to, message, password):
    port = config['MAIL'].get('port', 587)
    ssl = config['MAIL'].get('ssl', True)
    host = config['MAIL'].get('host', None)
    username = message['From']
    if None not in [host, username, password]:
        server = SMTP(host=host, port=port)
        if ssl:
            server.ehlo()
            server.starttls()
            server.ehlo()
        server.login(username, password)
        bcc = message.get('Bcc', [])
        if not isinstance(to, list):
            to = [to]
        if not isinstance(bcc, list):
            bcc = [bcc]
        to += bcc
        server.sendmail(username, to, message.as_string().encode('utf-8'))
