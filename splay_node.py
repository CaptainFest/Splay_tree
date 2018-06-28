class SplayNode(object):

    def __init__(self, data):
        """setters"""
        self._data = data
        self._par = None
        self._leftChild = None
        self._rightChild = None

    @property
    def data(self):
        return self._data

    @property
    def par(self):
        return self._par

    @property
    def leftChild(self):
        return self._leftChild

    @property
    def rightChild(self):
        return self._rightChild
