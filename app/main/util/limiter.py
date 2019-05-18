import redis
from flask import request, current_app
from functools import wraps

r = redis.Redis(decode_responses=True)


def rate_limited(fn=None, limit=20, methods=None, ip=True, minutes=1):
    """Limits requests to this endpoint to `limit` per `minutes`."""

    if methods is None:
        methods = []
    if not isinstance(limit, int):
        raise Exception('Limit must be an integer number.')
    if limit < 1:
        raise Exception('Limit must be greater than zero.')

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            enabled = current_app.config.get('ENABLE_REQUESTS_LIMITER')
            if (not methods or request.method in methods) and enabled:

                if ip:
                    increment_counter(for_methods=methods, minutes=minutes)
                    count = get_count(for_methods=methods)
                    if count > limit:
                        response_object = {
                            'status': 'error',
                            'message': 'Too many requests.'
                        }
                        return response_object, 429

            return func(*args, **kwargs)

        return inner
    return wrapper(fn) if fn else wrapper


def get_counter_key(for_only_this_route=True, for_methods=None):
    if not isinstance(for_methods, list):
        for_methods = []
    key = request.remote_addr
    route = ''
    if for_only_this_route:
        route = '{endpoint}'.format(
            endpoint=request.endpoint,
        )
    return "{methods}-{key}{route}".format(
        key=key,
        methods=','.join(for_methods),
        route=route,
    )


def increment_counter(for_only_this_route=True, for_methods=None, minutes=1):

    key = get_counter_key(for_only_this_route=for_only_this_route, for_methods=for_methods)
    try:
        r.incr(key)
        r.expire(key, time=60 * minutes)
    except Exception as e:
        print("Limiter error: {}".format(e))
        pass


def get_count(for_only_this_route=True, for_methods=None):
    key = get_counter_key(for_only_this_route=for_only_this_route, for_methods=for_methods)
    try:
        return int(r.get(key) or 0)
    except Exception as e:
        print("Limiter error: {}".format(e))
        return 0
