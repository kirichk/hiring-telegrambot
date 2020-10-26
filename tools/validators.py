import functools
import sentry_sdk
import validators


def logger_factory(logger):
    """ Импорт функции происходит раньше чем загрузка конфига логирования.
        Поэтому нужно явно указать в какой логгер мы хотим записывать.
    """
    def debug_requests(func):

        @functools.wraps(func)
        def inner(*args, **kwargs):

            try:
                logger.debug('Обращение в функцию `{}`'.format(func.__name__))
                return func(*args, **kwargs)
            except Exception as exc:
                logger.exception('Ошибка в функции `{}`'.format(func.__name__))
                sentry_sdk.capture_exception(error=exc)
                raise

        return inner

    return debug_requests


def link_validators(link):
    return validators.url.url(link)
