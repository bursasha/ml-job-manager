#


class BaseError(Exception):
    """
    Base class for all application-defined errors.
    """

    message = ""

    def __init__(self, detail: str) -> None:
        """
        Initialize the error with a detailed context message.

        Parameters:
            detail (str): Additional information about the specific error instance.
        """

        super().__init__(f"{self.message} {detail}")
