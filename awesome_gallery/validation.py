import logging
import os

from lxml import etree

from odoo.loglevels import ustr
from odoo.tools import misc, view_validation

_logger = logging.getLogger(__name__)

_gallery_validation = None


@view_validation.validate('gallery') 
def schema_gallery(arch, **kwargs):
    """ Check the gallery view against its schema

    :type arch: etree._Element
    """
    global _viewname_validator

    if _viewname_validator is None:
        with misc.file_open(os.path.join('modulename', 'rng', 'viewname.rng')) as f:
            _viewname_validator = etree.RelaxNG(etree.parse(f))

    if _viewname_validator.validate(arch):
        return True

    for error in _viewname_validator.error_log:
        _logger.error(ustr(error))
    return False
