"""
Convert dictionary to object based on chain
"""


class Bunch(dict):
    """
    Convert dictionary to object
    """

    def __getattr__(self, key):
        """
        Get value by key
        """
        if key in self:
            return self[key]
        else:
            raise AttributeError(f'No such attribute: {key}')

    def __setattr__(self, key, value):
        """
        Set key and value
        """
        self[key] = value

    def __delattr__(self, key):
        """
        Delete value by key
        """
        if key in self:
            del self[key]
        else:
            raise AttributeError(f'No such attribute: {key}')
