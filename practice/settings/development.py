from .base import *  # noqa:F403

DEBUG = True

INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS += [  # noqa:F405
        'debug_toolbar',
    ]

MIDDLEWARE += [  # noqa:F405
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
