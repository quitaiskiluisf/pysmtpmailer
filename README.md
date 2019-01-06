# pysmtpmailer

SMTP client for sending e-mails from the command line. Uses Python's internal smtplib module. For Python 3.0+.

## Usage:

```
usage: pysmtpmailer.py [-h] [--version] [-S SMTP_SERVER_ADDRESS]
                       [-p SMTP_SERVER_PORT] [-U SMTP_SERVER_USERNAME]
                       [-P SMTP_SERVER_PASSWORD] [-f FROM_ADDRESS] -t
                       [MAIL_ADDRESS [MAIL_ADDRESS ...]]
                       [-c [MAIL_ADDRESS [MAIL_ADDRESS ...]]]
                       [-b [MAIL_ADDRESS [MAIL_ADDRESS ...]]] [-s SUBJECT]
                       [-m MESSAGE] [-a [FILE [FILE ...]]]

SMTP client for sending e-mails from the command-line

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -S SMTP_SERVER_ADDRESS, --smtp-server-address SMTP_SERVER_ADDRESS
                        SMTP server to use for sending the message. Default:
                        localhost.
  -p SMTP_SERVER_PORT, --smtp-server-port SMTP_SERVER_PORT
                        SMTP server port. Default: 25.
  -U SMTP_SERVER_USERNAME, --smtp-server-username SMTP_SERVER_USERNAME
                        Username supplied to the SMTP server. Default: empty.
  -P SMTP_SERVER_PASSWORD, --smtp-server-password SMTP_SERVER_PASSWORD
                        Password supplied to the SMTP server. Default: empty
                        Note: if both username and password arguments are
                        empty, no credentials will be sent to the server.
  -f FROM_ADDRESS, --from-address FROM_ADDRESS
                        The address which will be set on the mail "From: "
                        header. Default: empty.
  -t [MAIL_ADDRESS [MAIL_ADDRESS ...]], --to-address [MAIL_ADDRESS [MAIL_ADDRESS ...]]
                        The address which the message will be sent to. More
                        than one address may be supplied.
  -c [MAIL_ADDRESS [MAIL_ADDRESS ...]], --cc-address [MAIL_ADDRESS [MAIL_ADDRESS ...]]
                        Carbon copy destinations. Multiple addresses may be
                        specified.
  -b [MAIL_ADDRESS [MAIL_ADDRESS ...]], --bcc-address [MAIL_ADDRESS [MAIL_ADDRESS ...]]
                        Blind carbon copy destinations. Multiple addresses may
                        be specified.
  -s SUBJECT, --subject SUBJECT
                        Subject of the message. By default, the first line of
                        the message is regarded as the subject. Setting this
                        argument ensures that everything specified on the body
                        is effectively sent in the body of the message.
  -m MESSAGE, --message MESSAGE
                        Body of the message. Note: at least the subject or the
                        message must be supplied.
  -a [FILE [FILE ...]], --attachment [FILE [FILE ...]]
                        Files which must be sent as attachments to the
                        message. Multiple files may be specified.
```
