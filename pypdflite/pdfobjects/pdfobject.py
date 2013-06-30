

class _PDFObject(object):
    """ Mainly used in Session, to maintain
        ids and byte counts for the objects
        in session.buffer.

    """
    def __init__(self, myid, offset):
        self.id = myid
        self.offset = offset
