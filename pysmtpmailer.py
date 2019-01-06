#! /usr/bin/env python3

import argparse
import email.message
import mimetypes
import os.path
import smtplib

def _get_file_content(file):
    '''Returns a tuple: the file's mimetype and the file content as a bytes
       array'''
    with open(file, mode='rb') as f:
        return (mimetypes.guess_type(file)[0], f.read(), )


def parse_args():
    '''Declares and parses the command-line arguments. Returns a dict with all
       of the options set by the user.'''
    description = 'SMTP client for sending e-mails from the command-line'
    p = argparse.ArgumentParser(description=description, )
    p.add_argument('--version', action='version', version='%(prog)s DEV', )
    p.add_argument('-S', '--smtp-server-address', default='localhost',
                   help='SMTP server to use for sending the message. Default: \
                         localhost.',
    )
    p.add_argument('-p', '--smtp-server-port', type=int, default=25,
                   help='SMTP server port. Default: 25.',
    )
    p.add_argument('-U', '--smtp-server-username', default='',
                   help='Username supplied to the smtp server. Default: empty.',
    )
    p.add_argument('-P', '--smtp-server-password', default='',
                   help='Password supplied to the smtp server. Default: empty\
                         Note: if both username and password arguments are \
                         empty, no credentials will be sent to the server.',
    )
    p.add_argument('-f', '--from-address', default='',
                   help='The address which will be set on the mail "From: " \
                         header. Default: empty.',
    )
    p.add_argument('-t', '--to-address', required=True, nargs='*',
                   metavar='MAIL_ADDRESS', default=[],
                   help='The address which the message will be sent to. More \
                         than one address may be supplied.',
    )
    p.add_argument('-c', '--cc-address', nargs='*', metavar='MAIL_ADDRESS',
                   default=[],
                   help='Carbon copy destinations. Multiple addresses may be \
                         specified.',
    )
    p.add_argument('-b', '--bcc-address', nargs='*', metavar='MAIL_ADDRESS',
                   default=[],
                   help='Blind carbon copy destinations. Multiple addresses \
                         may be specified.',
    )
    p.add_argument('-s', '--subject', default=None,
                   help='Subject of the message. By default, the first line of \
                         the message is regarded as the subject. Setting this \
                         argument ensures that everything specified on the \
                         body is effectively sent in the body of the message.',
    )
    p.add_argument('-m', '--message', default=None,
                   help='Body of the message.\
                         Note: at least the subject or the message must be \
                         supplied.',
    )
    p.add_argument('-a', '--attachment', nargs='*', metavar='FILE', default=[],
                   help='Files which must be sent as attachments to the \
                         message. Multiple files may be specified.',
    )

    options = vars(p.parse_args())

    # Extra processing for the parameters

    # Validates that at least the subject or the message were supplied
    if options['subject'] == None and options['message'] == None:
        raise Exception('At least one of the following options must be \
                         supplied: subject, message')

    # Set the first line of the message as the subject of the message, if no
    # subject was provided
    if options['subject'] == None:
        values = options['message'].split('\n', maxsplit=1)
        if len(values) == 2:
            options['subject'] = values[0]
            options['message'] = values[1]

    # Load the files.
    # At first, the path and the filename are separated from each other, and
    # the name part is cheched for uniqueness. If everything is ok, the file
    # content is loaded and the 'attachment' directive is replaced by a list of
    # tuples, where each tuple stores the file name as first element, the
    # detected mimetype as second and the file content (as a bytes array) on
    # the third.
    # Any error found will halt the process and terminate the execution.
    files = {}

    for file in options['attachment']:
        if not os.path.isfile(file):
            raise Exception('The file {} was not found'.format(file))

        file_path, file_name = os.path.split(file)
        if file_name in files:
            msg = 'The file {} was specified multiple times'.format(file_name)
            raise Exception(msg)

        files[file_name] = file_path

    options['attachment'] = []
    for file_name, file_path in files.items():
        full_file_path = os.path.join(file_path, file_name)
        mime_type, file_content = _get_file_content(full_file_path)
        options['attachment'].append((file_name, mime_type, file_content, ))

    return options


def send_mail(smtp_server_address, smtp_server_port, smtp_server_username,
              smtp_server_password, from_address, to_address, cc_address,
              bcc_address, subject, message, attachment):
    '''Sends mail. Options implemented according to the description on the
       command-line parameters. '''

    # Build the message
    msg = email.message.EmailMessage()
    msg['From'] = from_address
    msg['To'] = ', '.join(to_address)
    if len(cc_address) > 0:
        msg['Cc'] = ', '.join(cc_address)
    if len(bcc_address) > 0:
        msg['Bcc'] = ', '.join(bcc_address)
    if subject != None:
        msg['Subject'] = subject
    if message != None:
        msg.set_content(message)

    for file_name, file_mimetype, file_content in attachment:
        if '/' not in file_mimetype:
            file_mimetype = 'application/octet-stream'

        main_type, subtype = file_mimetype.split('/', maxsplit=1)
        msg.add_attachment(file_content, maintype=main_type, subtype=subtype,
                           filename=file_name)

    with smtplib.SMTP(host=smtp_server_address, port=smtp_server_port) as srv:
        # Only authenticates if credentials were supplied on the command-line
        if smtp_server_username != '' or smtp_server_password != '':
            srv.login(user=smtp_server_username, password=smtp_server_password)

        srv.send_message(msg)


if __name__ == '__main__':
    send_mail(**parse_args())
