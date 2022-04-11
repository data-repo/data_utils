from data_tools.utils.logger import Logger

log = Logger()


class NotFoundException(Exception):
    """
    Exception 404
    """

    def __init__(self, message="Page not found"):
        self.message = message
        log.error(msg=message)
        super().__init__(self.message)


class BadRequestException(Exception):
    """
    Exception 400
    """

    def __init__(self, message="The server could not understand the request due to invalid syntax."):
        self.message = message
        log.error(msg=message)
        super().__init__(self.message)


class ForbiddenException(Exception):
    """
    Exception 403
    """

    def __init__(self, message="The client does not have access rights to the content"):
        self.message = message
        log.error(msg=message)
        super().__init__(self.message)


class TimeoutException(Exception):
    """
    Exception 408
    """

    def __init__(self, message="request time out"):
        self.message = message
        log.error(msg=message)
        super().__init__(self.message)


class TooManyRequestsException(Exception):
    """
    Exception 429
    """

    def __init__(self, message='The user has sent too many requests in a given amount of time rate limiting.'):
        self.message = message
        log.error(msg=message)
        super().__init__(self.message)
