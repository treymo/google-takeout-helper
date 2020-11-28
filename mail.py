"""
Module for extracting all attachments from an mbox archive.
"""

import mailbox
import os


def _get_attachments(message):
    """Returns a list of attachments in an email Message."""
    return [part for part in message.get_payload() if
            part.get_content_disposition() == 'attachment']

def _strip_illegal_char(string, seperator=''):
	string = str(string)
	parsed = re.sub(r'[\<,\>,\:,\",\/,\\,\|,\?,\*,\n,\t]', seperator, string)
	if string != parsed:
		print('Illegal windows char. Renamed "{}" to "{}"'.format(string, parsed))
	return parsed

def _write_attachment(attachment, mbox_file_path):
    """Writes the attached file to an output directory."""
    attachments_path = os.path.join(os.path.dirname(mbox_file_path),
                                    'extracted_attachments')
    if not os.path.isdir(attachments_path):
        os.mkdir(attachments_path)

	timestamp = str(int(time.time()))  # use on collisions
	filename = attachment.get_filename()
	if filename is None:
		return

	filename = _strip_illegal_char(filename)
	path = os.path.join(attachments_path, filename)
	# If same filename, append with unique string
	if os.path.exists(path):
		original_path = path
		path = os.path.join(attachments_path, timestamp + '-' + filename)
		print('Renamed "{}" to "{}"'.format(original_path, path))

	try:
		with open(path, 'wb') as fb:
			fb.write(attachment.get_payload(decode=True))
			print('Saved "{}"'.format(path))
	except Exception as e:
		print('Error: ' + e)
		return


def extract_mail_attachments(mbox_file_path):
    """Extracts and writes email attachments from an mbox archive."""
    mbox = mailbox.mbox(mbox_file_path)
    for message in mbox:
        # Right now I'm assuming attachments only exist on multipart messages. I
        # haven't read the specifications of the mbox file format.
        if message.is_multipart():
            for attachment in _get_attachments(message):
                _write_attachment(attachment, mbox_file_path)
                mbox = mailbox.mbox(mbox_file_path)
