import logging
import os

from lxml import etree

from odoo.loglevels import ustr
from odoo.tools import misc, view_validation

_logger = logging.getLogger(__name__)

_gallery_validator = None

@view_validation.validate('gallery')
def schema_gallery(arch, **kwargs):
    global _gallery_validator

    if _gallery_validator is None:
        with misc.file_open(os.path.join('awesome_gallery', 'rng', 'gallery.rng')) as f:
            _gallery_validator = etree.RelaxNG(etree.parse(f))

    if _gallery_validator.validate(arch):
        return True

    for error in _gallery_validator.error_log:
        _logger.error(ustr(error))
    return False
