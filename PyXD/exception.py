from requests import RequestException


class PyXDownloaderException(Exception):
    """Base exception for this script.

    :note: Pengecualian ini tidak boleh diajukan secara langsung.
    """
    pass


class HTTPErrorException(Exception):
    pass


class RequestProcessingError(RequestException):
    pass


class CSRFTokenMissingError(Exception):
    pass


class URLValidationError(Exception):
    pass


class FunctionNotFoundError(Exception):
    pass
