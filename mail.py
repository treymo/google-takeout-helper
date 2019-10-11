import mailbox
import os


def _get_attachments(message):
    """Returns a list of attachments in an email Message."""
    return [part for part in message.get_payload() if
            part.get_content_disposition() == 'attachment']


def _write_attachment(attachment, mbox_file_path):
    """Writes the attached file to an output directory."""
    attachments_path = os.path.join(os.path.dirname(mbox_file_path),
                                    'extracted_attachments')
    if not os.path.isdir(attachments_path):
        os.mkdir(attachments_path)

    fb = open(os.path.join(attachments_path, attachment.get_filename()), 'wb')
    fb.write(attachment.get_payload(decode=True))
    fb.close()


def extract_mail_attachments(mbox_file_path):
    """Extracts and writes email attachments from an mbox archive."""
    mbox = mailbox.mbox(mbox_file_path)
    for message in mbox:
        # Right now I'm assuming attachments only exist on multipart messages. I
        # haven't read the specifications of the mbox file format.
        if message.is_multipart():
            for attachment in _get_attachments(message):
                _write_attachment(attachment, mbox_file_path)
