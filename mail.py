import mailbox
import os

def extract_mail_attachments(mbox_file_path):
    mbox = mailbox.mbox(mbox_file_path)
    for message in mbox:
        # Right now I'm assuming attachments only exist on multipart messages. I
        # haven't read the specifications of the mbox file format.
        if message.is_multipart():
            message_parts = message.get_payload()
            for part in message_parts:
                if part.get_content_disposition() == 'attachment':
                    attachments_path = os.path.join(os.path.dirname(mbox_file_path),
                                                    'extracted_attachments')
                    if not os.path.isdir(attachments_path):
                        os.mkdir(attachments_path)

                    fb = open(os.path.join(attachments_path, part.get_filename()), 'wb')
                    fb.write(part.get_payload(decode=True))
                    fb.close()
