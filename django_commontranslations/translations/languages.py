# -*- coding: utf-8 -*-
"""
Language names that are not already translated in the Django package
"""
_ = lambda s: s

ALL_LANGUAGES = dict((
    ('es-ar', _('Argentinean Spanish')),
    ('no',    _('Norwegian')),
    ('de-ch', _('Swiss German')),
    ('fr-ch', _('Swiss French')),
))