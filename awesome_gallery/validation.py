# -*- coding: utf-8 -*-
import logging
import os

from lxml import etree

from odoo.loglevels import ustr
from odoo.tools import misc, view_validation

_logger = logging.getLogger(__name__)

_gallery_validator = None


@view_validation.validate('gallery')
def schema_gallery(arch, **kwargs):
    """ Check the gallery view against its schema

    :type arch: etree._Element
    """
    global _gallery_validator

    if _gallery_validator is None:
        with misc.file_open(os.path.join('awesome_gallery', 'rng', 'gallery.rng')) as f:
            _gallery_validator = etree.RelaxNG(etree.parse(f))

    if _gallery_validator.validate(arch):
        return True

    for error in _gallery_validator.error_log:
        _logger.error(ustr(error))
    return False
