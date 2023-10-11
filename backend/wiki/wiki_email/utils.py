from functools import wraps


def menage_email_sending_method(is_email_sending: bool):
    def decorator(f):
        @wraps(f)
        async def wrapped_f(self, *args, **kwargs):
            result = None

            if is_email_sending:
                result = await f(self, *args, **kwargs)

            return result

        return wrapped_f

    return decorator
