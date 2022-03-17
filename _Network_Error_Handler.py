
import requests
import time




#Keep running even when Internet connection temporarily breaks
class NetworkError(RuntimeError):
    pass


def retryer(func):
    retry_on_exceptions=(
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError
        )
    def inner(*args,**kwargs):
        for i in range(200):
            try:
                resgold=func(*args,**kwargs)
            except retry_on_exceptions:
                time.sleep(30)
                continue
            else:
                return resgold
        else:
            print("\nError: Unknown Network connection timeout issue.")
            raise NetworkError
    return inner



